<template>
  <div>
    <CContainer>
      <CRow>
        <div class="col-sm-9 col-md-7 col-lg-5 mx-auto content-center">
          <CCard class="card-signin my-5 m-3">
            <CCardBody>
              <h5 class="card-title text-center">Sign In</h5>
              <CForm @submit.prevent="onSubmit()">
                <div class="justify-items-center">
                  <CRow class="content-center">
                    <CInput
                      class="col-10"
                      placeholder="Email Address"
                      v-model="email"
                    />
                  </CRow>
                  <CRow class="content-center">
                    <CInput
                      class="col-10"
                      placeholder="Password"
                      type="password"
                      v-model="password"
                    />
                  </CRow>
                  <CRow class="content-center">
                    <CButton
                      :disabled="isLoginFetching"
                      type="submit"
                      color="primary"
                      class="px-4"
                    >
                      {{ !isLoginFetching ? "Sign in" : "Loading..." }}
                    </CButton>
                  </CRow>
                </div>
              </CForm>
              <hr class="my-4" />
              <div class="text-center">
                <h6 class="mb-3">OR</h6>
                <GoogleLogin
                  class="btn btn-lg btn-google btn-block"
                  :params="params"
                  :onSuccess="onSuccessGoogle"
                  :onFailure="onFailureGoogle"
                  >Sign in with Google</GoogleLogin
                >
                <div class="mt-3">
                  Not Registered? <a href="/signup">SignUp Now</a>
                </div>
              </div>
            </CCardBody>
          </CCard>
        </div>
      </CRow>
      <CToaster v-if="showToaster" :autohide="3000" position="bottom-right">
        <CToast :show="true" class="bg-danger text-white">{{
          toastMessage
        }}</CToast>
      </CToaster>
    </CContainer>
  </div>
</template>

<script>
import services from "@/services/services";
import GoogleLogin from "vue-google-login";

export default {
  name: "Login",
  components: {
    GoogleLogin,
  },
  data() {
    return {
      email: "",
      password: "",
      isLoginFetching: false,
      params: {
        client_id: "170378570980-ht4k9obd1ce0k4qjfa6phdp4gqjkispe",
      },
      renderParams: {
        width: 250,
        height: 50,
        longtitle: true,
      },
      showToaster: false,
      toastMessage: "",
    };
  },
  methods: {
    onSubmit() {
      let payload = {
        email: this.email,
        password: this.password,
      };
      this.login_accesstoken(payload);
    },
    login_accesstoken(payload) {
      this.isLoginFetching = true;
      return services
        .access_token(payload)
        .then((res) => console.log(res))
        .catch((err) => {
          this.showToasterNow(err.details);
          console.log(err);
        });
    },
    onSuccessGoogle(googleUser) {
      let user = googleUser.getBasicProfile();
      let login_type = "google";
      let payload = {
        email: user.$t,
        user_name: user.Ad,
      };
      return services.loginWith(login_type, payload).then((res) => {
        console.log(res);
      });
    },
    onFailureGoogle(googleUser) {
      console.log(googleUser);
    },
    showToasterNow(toastMessage) {
      this.toastMessage = toastMessage;
      this.showToaster = true;
      setInterval(() => {
        this.toastMessage = "";
        this.showToaster = false;
      }, 3000);
    },
  },
};
</script>

<style scoped>
:root {
  --input-padding-x: 1.5rem;
  --input-padding-y: 0.75rem;
}

.card-signin {
  border: 0;
  border-radius: 1rem;
  box-shadow: 0 0.5rem 1rem 0 rgba(0, 0, 0, 0.1);
  min-width: 450px;
}

@media only screen and (max-width: 480px) {
  .card-signin {
    min-width: 300px;
  }
}
.btn-google {
  color: white;
  background-color: #ea4335;
}

.btn-facebook {
  color: white;
  background-color: #3b5998;
}
</style>
