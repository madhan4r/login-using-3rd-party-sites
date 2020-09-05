<template>
  <CButton color="primary">
    Logout
  </CButton>
</template>

<script>
import services from "@/services/services";

export default {
  name: "Home",
  mounted() {
    return services.getByUser(2).then((res) => console.log(res));
  },
};
</script>
