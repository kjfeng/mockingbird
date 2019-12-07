function switchToSignup() {
  document.getElementsByClassName("login-title-wrapper")[0].style.display = "none";
  document.getElementsByClassName("login-form-wrapper")[ 0].style.display = "none";
  document.getElementsByClassName("signup-title-wrapper")[0].style.display = "block";
  document.getElementsByClassName("signup-form-wrapper")[0].style.display = "block";
}

function switchToRecovery() {
  document.getElementsByClassName("login-title-wrapper")[0].style.display = "none";
  document.getElementsByClassName("login-form-wrapper")[0].style.display = "none";
  document.getElementsByClassName("password-title-wrapper")[0].style.display = "block";
  document.getElementsByClassName("password-recovery-wrapper")[0].style.display = "block";
}

function displayPasswordConfirmation() {
  document.getElementsByClassName("login-title-wrapper")[0].style.display = "none";
  document.getElementsByClassName("login-form")[0].style.display = "none";
  document.getElementsByClassName("password-recovery-confirmation")[0].style.display = "block";
}

function switchToLogin() {
  document.getElementsByClassName("login-title-wrapper")[0].style.display = "block";
  document.getElementsByClassName("login-form-wrapper")[0].style.display = "block";
  document.getElementsByClassName("signup-title-wrapper")[0].style.display = "none";
  document.getElementsByClassName("signup-form-wrapper")[0].style.display = "none";
  document.getElementsByClassName("password-title-wrapper")[0].style.display = "none";
  document.getElementsByClassName("password-recovery-wrapper")[0].style.display = "none";
}

