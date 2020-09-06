<template>
  <div class="my-5">
    <h6>Username: {{ userData.user_name }}</h6>
    <h6>Email: {{ userData.email }}</h6>
    <h6>Login Type: {{ userData.login_type }}</h6>
    <h6>Gender: {{ gender }}</h6>
    <CRow class="content-center">
      <CButton variant="outline" size="sm" color="primary" @click="logout">
        Logout
      </CButton></CRow
    >
  </div>
</template>

<script>
import services from "@/services/services";

export default {
  name: "Home",
  data() {
    return {
      userData: "",
    };
  },
  computed: {
    gender() {
      return this.userData.gender ? this.userData.gender : "--";
    },
  },
  mounted() {
    let user = JSON.parse(window.localStorage.getItem("userdata"));
    user = this.parseJwt(user.access_token);
    if (user) {
      return services
        .getByID(user.data[0].user_id)
        .then((res) => (this.userData = res.data));
    } else {
      this.$router.push("/");
    }
  },
  methods: {
    logout() {
      window.localStorage.removeItem("userdata");
      this.$router.push("/");
    },
    parseJwt(token) {
      var base64Url = token.split(".")[1];
      var base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
      var jsonPayload = decodeURIComponent(
        atob(base64)
          .split("")
          .map(function(c) {
            return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
          })
          .join("")
      );

      return JSON.parse(jsonPayload);
    },
  },
};
</script>

<style scoped>
h6 {
  text-align: center;
}
</style>
