import { UserManager, User, type UserManagerSettings } from 'oidc-client-ts'

export default class AuthService {
  private userManager: UserManager

  private constructor(metadata: any) {
    let baseUrl = `${window.location.origin}${import.meta.env.BASE_URL}`
    // prevent problems when preview environments include trailing slash
    baseUrl = baseUrl.replace(/\/$/, "")
    const settings: UserManagerSettings = {
      authority: metadata["authority"] || "",
      client_id: metadata["client_id"] || "",
      redirect_uri: `${baseUrl}/auth_callback`,
      post_logout_redirect_uri: `${baseUrl}`,
      scope: 'openid',
    }
    this.userManager = new UserManager(settings)
  }

  static async instance(): Promise<AuthService> {
    let authMetadata = window.sessionStorage.getItem("authMetadata")

    if (authMetadata) {
      authMetadata = JSON.parse(authMetadata)
    } else {
      const apiBaseUrl = import.meta.env.PUBLIC_API_BASE_URL
      const metadataUrl = `${apiBaseUrl}/api/v1/auth/metadata`
      const metadataResponse = await fetch(metadataUrl)
      authMetadata = await metadataResponse.json()
      if (authMetadata) {
        window.sessionStorage.setItem("authMetadata", JSON.stringify(authMetadata))
      }
    }

    return new AuthService(authMetadata)
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
    return this.userManager.signoutSilent()
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
