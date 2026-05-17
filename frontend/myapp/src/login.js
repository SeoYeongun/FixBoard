export function setupLogin(container) {
  container.innerHTML = `
    <section class="login-page">
      <div class="login-card">
        <h1>로그인</h1>
        <p class="login-subtitle">계정에 로그인하세요</p>
        <form id="login-form" class="login-form" novalidate>
          <label class="login-field">
            <span>이메일</span>
            <input
              type="email"
              name="email"
              autocomplete="email"
              placeholder="you@example.com"
              required
            />
          </label>
          <label class="login-field">
            <span>비밀번호</span>
            <input
              type="password"
              name="password"
              autocomplete="current-password"
              placeholder="••••••••"
              minlength="6"
              required
            />
          </label>
          <label class="login-remember">
            <input type="checkbox" name="remember" />
            <span>로그인 상태 유지</span>
          </label>
          <p id="login-message" class="login-message" role="alert" hidden></p>
          <button type="submit" class="login-submit">로그인</button>
        </form>
        <p class="login-footer">
          계정이 없으신가요? <a href="#">회원가입</a>
        </p>
      </div>
    </section>
  `

  const form = container.querySelector('#login-form')
  const messageEl = container.querySelector('#login-message')

  const showMessage = (text, type = 'error') => {
    messageEl.textContent = text
    messageEl.hidden = false
    messageEl.dataset.type = type
  }

  const hideMessage = () => {
    messageEl.hidden = true
    messageEl.textContent = ''
    delete messageEl.dataset.type
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault()
    hideMessage()

    const data = new FormData(form)
    const email = String(data.get('email') ?? '').trim()
    const password = String(data.get('password') ?? '')

    if (!email || !password) {
      showMessage('이메일과 비밀번호를 입력해 주세요.')
      return
    }

    if (password.length < 6) {
      showMessage('비밀번호는 6자 이상이어야 합니다.')
      return
    }

    showMessage(`${email}으로 로그인되었습니다.`, 'success')
    form.reset()
  })
}
