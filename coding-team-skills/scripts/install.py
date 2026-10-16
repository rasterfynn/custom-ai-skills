"""Install the authored team skills without replacing unrelated personal settings."""

import argparse
import datetime
import pathlib
import re
import shutil
import tomllib


def write_if_changed(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == content:
        return False
    path.write_bytes(content)
    return True


def install(package, codex_home, project):
    config_path = codex_home / "config.toml"
    config_bytes = config_path.read_bytes() if config_path.exists() else b""
    config_text = config_bytes.decode("utf-8-sig")
    original = tomllib.loads(config_text)
    expected = tomllib.loads(config_text)
    for key in ("default_subagent_model", "default_subagent_reasoning_effort"):
        expected.get("agents", {}).pop(key, None)

    # Remove only these two settings from the personal [agents] table.
    # An omitted subagent model/effort then inherits the current parent values.
    in_agents = False
    kept = []
    for line in config_text.splitlines(keepends=True):
        if re.match(r"\s*\[", line):
            in_agents = bool(re.match(r"\s*\[agents\]\s*(?:#.*)?$", line))
        if in_agents and re.match(
            r"\s*default_subagent_(?:model|reasoning_effort)\s*=", line
        ):
            continue
        kept.append(line)
    updated_config = "".join(kept)
    assert tomllib.loads(updated_config) == expected, "Unexpected config change"
    if config_path.exists():
        assert config_path.read_bytes() == config_bytes, "Config changed during setup"

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    if original != expected:
        backup = config_path.with_name(config_path.name + ".before-team-skills-" + stamp)
        shutil.copy2(config_path, backup)
        write_if_changed(config_path, updated_config.encode("utf-8"))
        print("Backed up personal config:", backup)

    count = 0
    for category in ("skills", "agents"):
        for source in sorted((package / category).rglob("*")):
            if source.is_file():
                count += write_if_changed(
                    codex_home / category / source.relative_to(package / category),
                    source.read_bytes(),
                )

    routing_path = codex_home / "AGENTS.md"
    routing_bytes = routing_path.read_bytes() if routing_path.exists() else b""
    routing_text = routing_bytes.decode("utf-8-sig")
    start = "<!-- coding-team-skills:start -->"
    end = "<!-- coding-team-skills:end -->"
    assert routing_text.count(start) == routing_text.count(end), "Incomplete routing markers"
    assert routing_text.count(start) <= 1, "Duplicate routing blocks"
    block = start + "\n" + (package / "AGENTS.md").read_text(encoding="utf-8").strip() + "\n" + end
    if start in routing_text:
        before, rest = routing_text.split(start, 1)
        _, after = rest.split(end, 1)
        routing_updated = before + block + after
    else:
        routing_updated = routing_text.rstrip() + ("\n\n" if routing_text.strip() else "") + block + "\n"
    if routing_updated.encode("utf-8") != routing_bytes:
        if routing_bytes:
            shutil.copy2(routing_path, routing_path.with_name("AGENTS.md.before-team-skills-" + stamp))
        count += write_if_changed(routing_path, routing_updated.encode("utf-8"))

    # Existing project roles override personal roles of the same name. Update only
    # roles already present in the specifically supplied project, not other projects.
    synchronized = 0
    if project is not None:
        for source in sorted((package / "agents").glob("*.toml")):
            target = project / ".codex" / "agents" / source.name
            if target.exists():
                synchronized += write_if_changed(target, source.read_bytes())

    print("Personal skill/agent/routing files changed:", count)
    print("Existing project role files synchronized:", synchronized)
    print("Installed skills: coding-teams, dev-lite, dev, dev-high, simple-work")
    print("Installed roles: 18 team roles and single_worker")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=pathlib.Path, required=True)
    parser.add_argument("--sync-project", type=pathlib.Path)
    arguments = parser.parse_args()
    install(
        pathlib.Path(__file__).resolve().parents[1],
        arguments.codex_home.resolve(),
        arguments.sync_project.resolve() if arguments.sync_project else None,
    )
