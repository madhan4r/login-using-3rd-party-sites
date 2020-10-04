<template>
  <div>
    <Header :userProfile="userProfile" />
    <AdminHome
      v-if="isAdmin"
      :userProfile="userProfile"
      @toaster="showToasterNow"
    />
    <UserHome
      v-else
      :userProfile="userProfile"
      @toaster="showToasterNow"
      @getMe="me"
    />
    <CToaster v-if="showToaster" :autohide="3000" position="bottom-right">
      <CToast :show="true" class="bg-danger text-white">{{
        toastMessage
      }}</CToast>
    </CToaster>
  </div>
</template>

<script>
import Header from "@/components/Header";
import AdminHome from "@/components/AdminHome";
import UserHome from "@/components/UserHome";
import services from "@/services/services";

export default {
  name: "HomePage",
  components: {
    AdminHome,
    UserHome,
    Header
  },
  data() {
    return {
      user: "",
      userProfile: "",
      showToaster: false,
      toastMessage: ""
    };
  },
  mounted() {
    let data = this.userData();
    data ? (this.user = data.data[0]) : null;
    if (this.user) {
      this.me(this.user.user_id);
    } else {
      this.$router.push("/");
    }
  },
  computed: {
    isAdmin() {
      return this.user.userRole == "admin" ? true : false;
    }
  },
  methods: {
    me(user_id) {
      return services.getByID(user_id).then(res => {
        this.userProfile = res.data;
      });
    },
    userData() {
      let user = JSON.parse(window.localStorage.getItem("userdata"));
      if (user) {
        var base64Url = user.access_token.split(".")[1];
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
      }
      return false;
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
