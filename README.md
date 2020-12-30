# AppleSignIn
## Ionic  Cordova 

ionic cordova plugin add cordova-plugin-sign-in-with-apple
npm install @ionic-native/sign-in-with-apple

> WAGNING: Имя пользователя будет доступно только при первом обращении

```
constructor(private signInWithApple: SignInWithApple) {}


loginWithApple() {
    this.signInWithApple.signin({
        requestedScopes: [
        ASAuthorizationAppleIDRequest.ASAuthorizationScopeFullName,
        ASAuthorizationAppleIDRequest.ASAuthorizationScopeEmail
        ]
    })
    .then((res: AppleSignInResponse) => {
        // TODO: send res.identityToken to server 
        console.log(res);
    })
    .catch((error: AppleSignInErrorResponse) => {
        console.error(error);
    });
}
```


## Back-end
[Apple Documentation](https://developer.apple.com/documentation/sign_in_with_apple/sign_in_with_apple_rest_api/authenticating_users_with_sign_in_with_apple)

![img](https://docs-assets.developer.apple.com/published/360d59b776/rendered2x-1592224731.png)

1. **Create apple Config**
    ```
    Config : {
        TeamID      string      //ID с сайта developer.apple.com
        ClientID    string      //Bundle iOS приложения
        RedirectURI string      //ссылка для редиректа при успешной авторизации (not required)
        KeyID       string      //Сгенерированный ключ с сайта developer.apple.com
        AESCert     interface{} //Сертификат для подписи
    }
    ```
2. **Read Cert**  
    [Documentatin (Create PRIVATE_KEY)](https://help.apple.com/developer-account/#/devcdfbb56a3)
    ```
    PRIVATE_KEY: []bytes = '****'
    block = encode(PRIVATE_KEY)

    Config.AESCert = x509.ParsePKCS8PrivateKey(block)
    ```

3. **Get Apple Tocken**  
[Docuentation](https://developer.apple.com/documentation/sign_in_with_apple/generate_and_validate_tokens)  

    Input:  
    ```
    ClientTocken : string
    ```
    Output:  
    ```
    AppleToken : {
        access_token  string,
        expires_in    int64,
        id_token      string,
        refresh_token string,
        token_type    string
    }
    AppleToken.id_tocken : jwt : {
        sub string,
        email string,
        email_verified bool
    }
    ```
    Steps:  
    ```
    token = jwt.New("ES256", {
        "iss": Config.TeamID,
        "iat": time.Now().Unix(),
        "exp": time.Now().Unix() + expireTime,
        "aud": "https://appleid.apple.com",
        "sub": Config.ClientID,
    })

    token.Header = {
        "kid": Config.KeyID,
        "alg": "ES256",
    }

    tokenString = token.SignedString(Config.AESCert)

    resp = request.Post("https://appleid.apple.com/auth/token", {
        "client_id": Config.ClientID,
        "client_secret": tokenString,
        "code": ClientTocken,
        "grant_type": "authorization_code",
        "redirect_uri": Config.RedirectURI,
    })

    appleTocken = (AppleToken)resp
    ```
