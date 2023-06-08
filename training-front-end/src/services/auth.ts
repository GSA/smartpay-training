import { UserManager, WebStorageStateStore, User, UserManagerSettings } from 'oidc-client-ts';

export default class AuthService {
  private userManager: UserManager;

  constructor() {
    const settings: UserManagerSettings = {
      userStore: new WebStorageStateStore({ store: window.sessionStorage }),
      // TODO: retrieve these values from a metadata endpoint?
      authority: 'http://localhost:8080/uaa',
      client_id: 'test_client_id',
      redirect_uri: 'http://localhost:3000/auth_callback',
      response_type: 'code',
      post_logout_redirect_uri: 'http://localhost:3000',
      scope: 'openid',
    };

    this.userManager = new UserManager(settings);
  }

  public getUser(): Promise<User | null> {
    return this.userManager.getUser();
  }

  public login(): Promise<void> {
    return this.userManager.signinRedirect();
  }

  public loginCallback(): Promise<User> {
    return this.userManager.signinRedirectCallback()
  }

  public logout(): Promise<void> {
    return this.userManager.signoutRedirect()
  }

  public getAccessToken(): Promise<string> {
    return this.userManager.getUser().then((data: any) => {
      return data.access_token;
    });
  }
}
