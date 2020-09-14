<template>
  <div>
    <CButton class="btn btn-facebook ml-2 mt-2" @click="buttonClicked">
      Sign in with Facebook
    </CButton>
  </div>
</template>
<script>
import {
  loadFbSdk,
  getLoginStatus,
  fbLogout,
  fbLogin,
} from "@/components/fbhelpers.js";
export default {
  name: "facebook-login",
  data() {
    return {
      isWorking: false,
      isConnected: false,
    };
  },
  methods: {
    buttonClicked() {
      this.login();
      // this.isConnected ? this.logout() : this.login();
    },
    logout() {
      this.isWorking = true;
      fbLogout().then((response) => {
        this.isWorking = false;
        this.isConnected = false;
        this.$emit("logout", response);
      });
    },
    login() {
      this.isWorking = true;
      fbLogin(this.loginOptions).then((response) => {
        if (response.status === "connected") {
          this.isConnected = true;
        } else {
          this.isConnected = false;
        }
        this.isWorking = false;
        this.$emit("login", {
          response,
          FB: window.FB,
        });
      });
    },
  },
  props: {
    appId: {
      type: String,
      required: true,
    },
    version: {
      type: String,
      default: "v2.10",
    },
    logoutLabel: {
      type: String,
      default: "Log out from Facebook",
    },
    loginLabel: {
      type: String,
      default: "Log In To Facebook",
    },
    loginOptions: {
      type: Object,
      default: function() {
        return {
          scope: "email",
        };
      },
    },
  },
  mounted() {
    this.isWorking = true;
    loadFbSdk(this.appId, this.version)
      .then(() => getLoginStatus())
      .then((response) => {
        if (response.status === "connected") {
          this.isConnected = true;
        }
        this.isWorking = false;
        /** get-initial-status to be depcreated on next major version */
        this.$emit("get-initial-status", response);
        this.$emit("sdk-loaded", {
          isConnected: this.isConnected,
          FB: window.FB,
        });
      });
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.btn-facebook {
  color: white;
  background-color: #3b5998;
}
</style>
