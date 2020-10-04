<template>
  <div>
    <header class="c-header c-header-light px-3">
      <a class="c-header-brand"
        ><strong> Welcome {{ userName }} </strong></a
      >
      <ul class="c-header-nav mr-auto">
        <li class="c-header-nav-item active"></li>
      </ul>
      <button @click="logout" class="c-header-toggler inline my-2 my-lg-0">
        Logout
      </button>
    </header>
  </div>
</template>

<script>
export default {
  name: "Header",
  props: ["userProfile"],
  computed: {
    userName() {
      return this.userProfile.user_name ? this.userProfile.user_name : "User";
    }
  },
  methods: {
    logout() {
      window.localStorage.removeItem("userdata");
      this.$router.push("/");
    }
  }
};
</script>

<style scoped>
header {
  background-color: darkgray;
  font-size: 14px;
  color: black;
}
</style>
