import { UserManager, User, UserManagerSettings } from 'oidc-client-ts'

export default class AuthService {
  private userManager: UserManager

  constructor() {
    const settings: UserManagerSettings = {
      authority: import.meta.env.PUBLIC_AUTH_AUTHORITY_URL,
      client_id: import.meta.env.PUBLIC_AUTH_CLIENT_ID,
      redirect_uri: import.meta.env.PUBLIC_AUTH_REDIRECT_URL,
      post_logout_redirect_uri: import.meta.env.PUBLIC_AUTH_POST_LOGOUT_URL,
      scope: 'openid',
    }
    this.userManager = new UserManager(settings)
  }

  public getUser(): Promise<User | null> {
    return this.userManager.getUser()
  }

  public login(): Promise<void> {
    return this.userManager.signinRedirect()
  }

  public loginCallback(): Promise<User> {
    return this.userManager.signinRedirectCallback()
  }

  public logout(): Promise<void> {
    return this.userManager.signoutRedirect()
  }

  public async getAccessToken(): Promise<string> {
    const user = await this.userManager.getUser()
    if (user) {
      return user.access_token
    } else {
      return ""
    }
  }
}
