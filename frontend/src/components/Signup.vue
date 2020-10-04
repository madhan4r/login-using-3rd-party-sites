<template>
  <div>
    <CContainer>
      <CRow>
        <div class="col-sm-9 col-md-7 col-lg-5 mx-auto content-center">
          <CCard class="card-signup my-5 m-3">
            <CCardBody>
              <h5 class="card-title text-center">Sign Up</h5>
              <ValidationObserver ref="register" v-slot="{ handleSubmit }">
                <CForm @submit.prevent="handleSubmit">
                  <div class="justify-items-center">
                    <div class="mt-3">
                      <label class="label required">Username:</label><br />
                      <ValidationProvider rules="required" v-slot="{ errors }">
                        <span class="error_msg" id="error">{{
                          errors[0]
                        }}</span>
                        <CInput
                          name="user_name"
                          class="col-12 is-danger"
                          :class="{ 'is-danger': errors }"
                          v-model="payload.user_name"
                        />
                      </ValidationProvider>
                    </div>
                    <div class="mt-3">
                      <label class="label">Email:</label><br />
                      <ValidationProvider
                        rules="required|email"
                        v-slot="{ errors }"
                      >
                        <span class="error_msg" id="error">{{
                          errors[0]
                        }}</span>
                        <CInput class="col-12" v-model="payload.email" />
                      </ValidationProvider>
                    </div>
                    <div class="mt-3">
                      <label class="label">Gender:</label><br />
                      <ValidationProvider rules="required" v-slot="{ errors }">
                        <span class="error_msg" id="error">{{
                          errors[0]
                        }}</span>
                        <v-select
                          class="ml-3 mr-3"
                          :options="options['gender']"
                          v-model="payload.gender"
                        />
                      </ValidationProvider>
                    </div>
                    <div class="mt-3">
                      <label class="label">Password:</label><br />
                      <ValidationProvider
                        vid="confirm"
                        :rules="{
                          required: true,
                          password_length: 8,
                          password_strength: /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})/
                        }"
                        v-slot="{ errors }"
                      >
                        <span class="error_msg" id="error">{{
                          errors[0]
                        }}</span>
                        <CInput
                          class="col-12"
                          type="password"
                          v-model="payload.password"
                        />
                      </ValidationProvider>
                    </div>
                    <div class="mt-3">
                      <label class="label">Confirm Password:</label><br />
                      <ValidationProvider
                        rules="required|confirmed:confirm"
                        v-slot="{ errors }"
                      >
                        <span class="error_msg" id="error">{{
                          errors[0]
                        }}</span>
                        <CInput
                          class="col-12"
                          v-model="confirmPassword"
                          type="password"
                        />
                      </ValidationProvider>
                    </div>
                    <CRow class="content-center">
                      <CButton
                        :disabled="isFetching"
                        type="submit"
                        color="primary"
                        @click="onSubmit()"
                        class="px-4"
                      >
                        {{ !isFetching ? "Sign up" : "Loading..." }}
                      </CButton>
                    </CRow>
                  </div>
                </CForm>
              </ValidationObserver>
              <hr class="my-4" />
              <div class="text-center">
                <div class="mt-3">Registered? <a href="/">Signin Now</a></div>
              </div>
            </CCardBody>
          </CCard>
        </div>
      </CRow>
    </CContainer>
    <CToaster v-if="showToaster" :autohide="3000" position="bottom-right">
      <CToast :show="true" class="bg-danger text-white">{{
        toastMessage
      }}</CToast>
    </CToaster>
  </div>
</template>

<script>
import { extend } from "vee-validate";
import {
  required,
  email,
  confirmed,
  min,
  regex
} from "vee-validate/dist/rules";
import services from "@/services/services";

extend("required", { ...required, message: "This field is required" });
extend("email", { ...email, message: "Invalid email" });
extend("confirmed", {
  ...confirmed,
  message: "This field should match password"
});
extend("password_length", {
  ...min,
  message: "Password be atleast 8 characters"
});
extend("password_strength", {
  ...regex,
  message: "Password must have capitals, numbers and special characters"
});

export default {
  name: "Signup",
  data() {
    return {
      payload: {
        user_name: "",
        email: "",
        gender: "",
        password: ""
      },
      confirmPassword: "",
      isFetching: false,
      showToaster: false,
      toastMessage: ""
    };
  },
  computed: {
    options() {
      return {
        gender: ["Male", "Female", "Transgender"]
      };
    }
  },
  methods: {
    async onSubmit() {
      const isValid = await this.$refs.register.validate();
      Object.values(this.$refs.register.errors).flat();
      this.$emit("onSubmit", this.payload);
      if (!isValid) {
        return;
      } else {
        this.isFetching = true;
        this.payload.login_type = "normal";
        this.createUser(this.payload);
      }
    },
    createUser(payload) {
      this.isFetching = false;
      return services
        .createUser(payload)
        .then(res => {
          let toastMessage = "User Account Created";
          this.showToasterNow(toastMessage);
          this.$router.push("/");
          return res;
        })
        .catch(err => {
          this.showToasterNow(err.response.data.detail);
          console.log(err);
        });
    },
    showToasterNow(toastMessage) {
      this.toastMessage = toastMessage;
      this.showToaster = true;
      setInterval(() => {
        this.toastMessage = "";
        this.showToaster = false;
      }, 3000);
    }
  }
};
</script>

<style scoped>
:root {
  --input-padding-x: 1.5rem;
  --input-padding-y: 0.75rem;
}

.card-signup {
  border: 0;
  border-radius: 1rem;
  box-shadow: 0 0.5rem 1rem 0 rgba(0, 0, 0, 0.1);
  min-width: 600px;
}

.label {
  width: 95%;
  text-align: left;
  font-family: serif;
  font-size: medium;
}

.error_msg {
  width: 95%;
  color: red;
  text-align: left;
}

@media only screen and (max-width: 480px) {
  .card-signup {
    min-width: 300px;
  }
}
</style>
