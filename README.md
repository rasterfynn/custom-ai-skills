# Custom AI Skills

Codex에서 작업 성격에 맞는 개발 팀 또는 단일 작업자를 명시적으로 호출하기 위한 개인용 스킬 모음입니다.

**워크플로우를 지정하지 않으면 현재 에이전트가 직접 처리합니다.** `simple-work`를 지정하면 작업자 한 명에게 위임하고, `dev-lite`, `dev`, `dev-high`를 지정하면 해당 개발 팀의 워크플로우를 실행합니다.

이 저장소는 스킬, 커스텀 에이전트 TOML, 개인 라우팅 규칙을 함께 설치하는 묶음입니다. 스킬 파일만 복사하면 커스텀 역할 등록과 기본 라우팅까지 설치되지 않습니다.

## 제공하는 워크플로우

| 선택 | 동작 | 호출 예시 |
|---|---|---|
| 미지정 | 현재 에이전트가 직접 처리. 추가 에이전트 자동 생성 없음 | `이 코드를 설명해줘.` |
| `simple-work` | 현재 부모 모델·추론 강도를 상속하는 작업자 한 명 | `이 코드를 설명해줘. use simple-work` |
| `dev-lite` | 비교적 가벼운 모델 구성의 개발 팀 | `로그인 오류를 수정해줘. use dev-lite` |
| `dev` | 기본 개발 팀 | `검색 기능을 추가해줘. use dev` |
| `dev-high` | 높은 추론 강도와 Astra를 포함한 개발 팀 | `렌더링 구조를 개선해줘. use dev-high` |

[`coding-teams`](coding-team-skills/skills/coding-teams/SKILL.md)는 위 호출을 구분하는 라우팅 스킬입니다. 별도의 개발 팀은 아닙니다.

### 개발 팀의 작업 절차

`dev` 계열은 동일한 [개발 워크플로우](coding-team-skills/skills/coding-teams/references/development-workflow.md)를 사용하며 역할별 모델 구성이 다릅니다.

1. **병렬 분석:** 코드 구조, 실패 재현, 설계, API 조사 등 필요한 질문을 읽기 전용으로 나누어 조사합니다.
2. **분석 완료 후 계획:** 분석 결과를 모아 변경 범위와 검증 목표를 정합니다.
3. **단독 구현:** 한 명의 implementer만 소스·설정·테스트 정의를 수정합니다.
4. **독립 검토와 검증:** reviewer와 test_runner가 별도로 확인합니다. 수정이 필요하면 같은 implementer가 반영하고 필요한 검증을 다시 수행합니다.
5. **결과 보고:** 변경 파일, 검증 명령과 결과, 실패한 검증, 남은 위험을 정리합니다.

등록된 여섯 역할을 매번 모두 실행하지는 않습니다. 버그는 코드 추적과 실패 재현, 큰 설계 변경은 구조 조사와 설계 분석처럼 작업에 필요한 역할을 선택합니다. 질문·계획·리뷰만 요청하면 구현을 추가하지 않습니다.

## 에이전트와 모델 구성

모델과 추론 강도의 실제 설정 기준은 [`coding-team-skills/agents/*.toml`](coding-team-skills/agents)입니다. 스킬의 역할 표는 설명과 선택 지침이며 실행 설정을 대신하지 않습니다.

| 논리 역할 | `dev-lite` | `dev` | `dev-high` |
|---|---|---|---|
| code_mapper | `gpt-6.1-sol` / `low` | `gpt-6.1-sol` / `medium` | `gpt-6.1-sol` / `high` |
| test_runner | `gpt-5.6-luna` / `medium` | `gpt-6.1-sol` / `low` | `gpt-6-astra` / `medium` |
| architect | `gpt-6.1-sol` / `low` | `gpt-6.1-sol` / `high` | `gpt-6.1-sol` / `ultra` |
| docs_researcher | `gpt-6.1-sol` / `low` | `gpt-6.1-sol` / `high` | `gpt-6.1-sol` / `ultra` |
| reviewer | `gpt-6.1-sol` / `low` | `gpt-6.1-sol` / `xhigh` | `gpt-6-astra` / `xhigh` |
| implementer | `gpt-5.6-luna` / `medium` | `gpt-6.1-sol` / `low` | `gpt-6.1-sol` / `medium` |

`dev-lite`의 역할명에는 `_lite`, `dev-high`에는 `_high`가 붙습니다. 예를 들어 `code_mapper_lite`, `reviewer_high`입니다. `dev`는 접미사 없는 역할명을 사용합니다.

[`single_worker.toml`](coding-team-skills/agents/single_worker.toml)은 모델과 추론 강도를 고정하지 않습니다. 명시적으로 선택한 `simple-work`에서만 호출하며 부모 세션의 현재 설정을 상속합니다. 커스텀 역할과 전체 이력 복제를 함께 지정하는 조합을 피하기 위해 새 문맥으로 생성하고, 필요한 작업 문맥은 따로 전달합니다.

설치된 Codex와 계정에서 지정된 모델·추론 강도를 지원해야 합니다. 지원하지 않는 역할을 다른 모델로 자동 대체하지 않습니다. `light`는 TOML의 `low`, `midium`은 `medium`으로 정규화되어 있습니다.

## 설치

### 준비 사항

- 커스텀 에이전트와 로컬 스킬을 지원하는 Codex를 설치하고 본인 계정으로 로그인합니다.
- Python **3.11 이상**이 필요합니다. 설치기는 표준 라이브러리만 사용하므로 별도 Python 패키지는 필요하지 않습니다.
- Git으로 받거나 GitHub의 **Code → Download ZIP**으로 저장소 전체를 받습니다. 스킬 간 공통 문서 참조가 있으므로 폴더 구조를 유지합니다.

설치 및 스킬 검색은 Codex CLI `0.162.1`에서 확인했습니다. 다른 버전에서는 설치 후 `/skills` 또는 스킬 선택 목록에서 검색 여부를 확인하세요.

### Windows PowerShell

```powershell
git clone https://github.com/rasterfynn/custom-ai-skills.git
Set-Location custom-ai-skills

$teamCodexHome = if ($env:CODEX_HOME) {
    $env:CODEX_HOME
} else {
    Join-Path $env:USERPROFILE ".codex"
}

py -3 --version
py -3 .\coding-team-skills\scripts\install.py --codex-home "$teamCodexHome"
```

`py -3 --version` 결과가 3.11 이상인지 확인합니다. Python 실행 명령이 `python`인 환경에서는 `py -3` 대신 `python`을 사용합니다. ZIP으로 받았다면 압축을 푼 저장소 폴더에서 설치 명령을 실행합니다.

### macOS / Linux

Python 3.11 이상과 Codex를 준비한 뒤 같은 설치기를 사용할 수 있습니다. 아래 예시는 기본 홈 경로와 `CODEX_HOME` 설정을 모두 지원합니다. 플랫폼별 실제 실행은 별도로 확인해야 합니다.

```bash
git clone https://github.com/rasterfynn/custom-ai-skills.git
cd custom-ai-skills

python3 --version
python3 ./coding-team-skills/scripts/install.py \
  --codex-home "${CODEX_HOME:-$HOME/.codex}"
```

### 설치 위치와 변경 내용

이 설치기는 지정한 Codex 홈 아래에 다음 파일을 설치합니다.

```text
<Codex 홈>/
├─ AGENTS.md
├─ skills/
│  ├─ coding-teams/
│  ├─ simple-work/
│  ├─ dev-lite/
│  ├─ dev/
│  └─ dev-high/
└─ agents/
   ├─ single_worker.toml
   └─ ... 개발 팀 역할 TOML 18개
```

- 개인 `AGENTS.md`의 `coding-team-skills:start` / `coding-team-skills:end` 구간을 추가하거나 갱신합니다. 구간 밖의 기존 지침은 유지합니다.
- `simple-work`가 현재 부모 모델을 상속하도록 개인 `config.toml`의 `[agents]`에서 `default_subagent_model`과 `default_subagent_reasoning_effort` 두 고정 기본값을 제거합니다. 다른 설정은 유지합니다.
- 위 변경이 발생할 때 기존 공통 설정과 비어 있지 않은 `AGENTS.md`를 같은 디렉터리에 `*.before-team-skills-*` 이름으로 백업합니다.
- **동일한 경로의 스킬·역할 파일은 교체될 수 있습니다.** 이 파일들에 개인 수정이 있다면 설치 전 별도로 보관하세요. 스킬·역할 파일 전체를 자동 백업하는 설치기는 아닙니다.
- 설치를 다시 실행하면 설치 대상 파일을 현재 저장소 버전과 맞춥니다. 내용이 같으면 다시 쓰지 않습니다.
- 없는 `config.toml`을 새로 만들거나 Fast 모드를 자동으로 활성화하지는 않습니다.

### 기존 프로젝트의 역할 파일 동기화

프로젝트 `.codex/agents`의 동명 역할은 개인 공통 역할을 가릴 수 있습니다. 해당 프로젝트에 **이미 있는 동명 역할 파일만** 이 묶음과 맞추려면 선택 옵션을 사용합니다.

```powershell
py -3 .\coding-team-skills\scripts\install.py `
  --codex-home "$teamCodexHome" `
  --sync-project "D:\work\my-project"
```

동기화 대상 프로젝트 파일도 교체될 수 있습니다. 다른 이름의 역할 파일은 변경하지 않습니다.

### Fast 모드 설정 — 선택 사항

Fast 모드의 서비스 등급은 부모 세션에서 하위 에이전트로 상속됩니다. 역할 TOML에 Fast를 적는 방식으로 개별 에이전트의 등급을 바꾸지 않습니다.

기본으로 사용하려면 개인 또는 프로젝트 `config.toml`에 아래 값을 **기존 설정과 병합**합니다. `service_tier`는 최상위에 두고 기존 `[features]`, `[agents]` 테이블을 중복 생성하지 않습니다.

```toml
service_tier = "fast"

[features]
fast_mode = true

[agents]
enabled = true
```

Fast의 실제 제공 여부와 사용량 계산은 계정·모델·클라이언트에 따릅니다. [공식 Speed 안내](https://learn.chatgpt.com/docs/agent-configuration/speed)를 참고하세요.

## 사용 방법

설치 후 Codex를 재시작하고 새 채팅을 여세요. CLI·IDE에서는 `/skills` 또는 `$`로 스킬을 선택할 수 있습니다. 선택 UI는 사용하는 클라이언트에 따라 다릅니다.

```text
# 직접 처리: 추가 에이전트 자동 생성 없음
이 함수가 무엇을 하는지 설명해줘.

# 단일 작업자 한 명에게 위임
이 함수가 무엇을 하는지 설명해줘. use simple-work

# 가벼운 개발 팀
로그인 오류를 수정해줘. use dev-lite

# 기본 개발 팀
검색 결과 정렬 기능을 추가해줘. use dev

# 높은 추론 강도의 개발 팀
데이터 처리 파이프라인의 설계를 검토해줘. use dev-high
```

직접 스킬을 지정하는 형식도 사용할 수 있습니다.

```text
$simple-work 이 코드를 설명해줘.
$dev-lite 로그인 오류를 수정해줘.
$dev 현재 변경 사항을 리뷰해줘.
$dev-high 공개 API 변경의 영향 범위를 조사해줘.
```

`/simple-work`, `/dev-lite`, `/dev`, `/dev-high`는 **클라이언트가 메시지 텍스트로 전달할 때 인식하는 별칭**입니다. 이 설치기가 내장 슬래시 명령을 등록하지는 않습니다. 클라이언트가 명령을 가로채면 `use 이름` 또는 `$이름`을 사용하세요.

선택한 워크플로우는 같은 작업의 후속 요청에서 유지됩니다. 새 독립 요청에 선택자가 없으면 직접 처리로 돌아갑니다. 명시적인 변경·취소 요청을 우선합니다. 팀 이름이 문서·인용·설명에 등장하는 것만으로 팀을 실행하지 않습니다.

## 업데이트

저장소를 받은 폴더에서 최신 내용을 받은 다음 설치기를 다시 실행합니다.

```powershell
git pull --ff-only
py -3 .\coding-team-skills\scripts\install.py --codex-home "$teamCodexHome"
```

다시 연 PowerShell에서는 설치 단계처럼 `$teamCodexHome`을 먼저 설정합니다. ZIP 사용자도 새 ZIP을 받은 뒤 같은 설치기를 실행할 수 있습니다. 변경된 설정을 적용하려면 새 채팅 또는 Codex 재시작이 필요할 수 있습니다.

## 확인 및 문제 해결

- **스킬이 보이지 않음:** `--codex-home` 경로, `CODEX_HOME`, 설치된 파일을 확인하고 Codex를 재시작합니다. 이 묶음의 설치 위치는 `<Codex 홈>/skills`입니다. 클라이언트 버전별 스킬 검색 경로는 [공식 Build skills 안내](https://learn.chatgpt.com/docs/build-skills)를 확인하세요.
- **역할을 찾지 못함:** `<Codex 홈>/agents`의 TOML과 프로젝트의 동명 역할 파일을 확인하고 새 채팅에서 다시 시도합니다.
- **모델·추론 강도를 지원하지 않음:** 계정과 설치 버전의 지원 목록을 확인합니다. 모델을 바꾸려면 해당 역할 TOML을 수정하고 문서의 설명도 맞춥니다. 자동 대체를 전제로 하지 않습니다.
- **현재 모델을 상속하지 않음:** 개인뿐 아니라 프로젝트·관리 설정에 고정된 서브에이전트 기본값이 있는지 확인합니다. 설치기는 개인 기본값 두 개만 제거하며 활성 세션이나 관리 정책을 덮어쓰지 않습니다.
- **실행 정책이 스킬 읽기나 도구 실행을 차단함:** 선택한 워크플로우는 차단 사유를 보고해야 합니다. 일반 답변으로 대체한 결과를 팀 실행 성공으로 보지 않습니다. 허용된 환경과 권한에서 다시 확인하세요.
- **직접 처리 확인:** 선택자 없이 짧은 질문을 보내 추가 에이전트가 생성되지 않는지 확인합니다.
- **단일 작업자 확인:** `2+2를 알려줘. use simple-work`를 보내 실제 생성·완료 기록에 한 작업자만 있는지 확인합니다.
- **개발 팀 확인:** 읽기 전용 분석 요청에 `use dev-lite`를 붙여 필요한 역할이 병렬로 분석하고 파일을 수정하지 않는지 확인합니다. 설정 유효성만으로 모든 모델의 실행 성공이 보장되지는 않습니다.

## 저장소 구조

```text
custom-ai-skills/
├─ README.md
├─ LICENSE
└─ coding-team-skills/
   ├─ AGENTS.md
   ├─ agents/                   # 모델·추론 강도·역할 지침
   ├─ scripts/install.py        # 개인 공통 설치 및 갱신
   └─ skills/
      ├─ coding-teams/          # 선택 규칙과 공유 개발 워크플로우
      ├─ simple-work/           # 명시적인 단일 작업자 위임
      ├─ dev-lite/
      ├─ dev/
      └─ dev-high/
```

## 참고 문서

- [OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI — Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [OpenAI — Speed](https://learn.chatgpt.com/docs/agent-configuration/speed)

## 라이선스

기존 저장소의 [MIT License](LICENSE)를 따릅니다.
