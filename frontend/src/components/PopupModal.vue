<template>
  <div class="pl-2">
    <CModal
      :title="modalTitle"
      :color="modalColor"
      :show.sync="isShowModal"
      :closeOnBackdrop="closeOnBackdrop"
    >
      <template #header>
        <h5>{{ modalTitle }}</h5>
        <button aria-label="Close" class="close" @click="modalCallBack(false)">
          x
        </button>
      </template>
      <CRow class="content-center">{{ modalContent }}</CRow>
      <div v-if="modalType == 'respond'">
        <CRow class="mt-3">
          <CCol>
            <label>Respond:</label>
          </CCol>
          <CCol>
            <v-select
              style="max-height: 31px;"
              :options="options['respond']"
              v-model="response"
            />
            <span v-if="showError" class="err_msg">This field is required</span>
          </CCol>
        </CRow>
        <CRow class="mt-3">
          <CCol>
            <label>Comments:</label>
          </CCol>
          <CCol>
            <CInput style="max-height: 31px;" v-model="comments" />
          </CCol>
        </CRow>
      </div>
      <div v-if="modalType == 'newApartment'">
        <CRow class="mt-3">
          <CCol>
            <label>Apartment Name:</label>
          </CCol>
          <CCol>
            <CInput style="max-height: 31px;" v-model="apartment_name" />
            <span v-if="showError" class="err_msg">This field is required</span>
          </CCol>
        </CRow>
        <CRow class="mt-3">
          <CCol>
            <label>Description:</label>
          </CCol>
          <CCol>
            <textarea v-model="description"></textarea>
          </CCol>
        </CRow>
      </div>
      <template #footer>
        <CRow class="justify-content-right">
          <CButton class="mr-2" color="secondary" @click="modalCallBack(false)"
            >Cancel</CButton
          >
          <CButton :color="modalColor" @click="submit">Save</CButton>
        </CRow>
      </template>
    </CModal>
  </div>
</template>
<script>
export default {
  name: "PopupModal",
  props: [
    "modalTitle",
    "modalColor",
    "modalContent",
    "isShowPopup",
    "modalCallBack",
    "closeOnBackdrop",
    "modalType",
  ],
  data() {
    return {
      isShow: this.isShowPopup,
      response: "",
      comments: "",
      apartment_name: "",
      description: "",
      showError: false,
    };
  },
  watch: {
    isShowPopup(newVal) {
      this.isShow = newVal;
      this.clearFields();
    },
  },
  computed: {
    isShowModal: {
      get() {
        return this.isShow;
      },
      set(isShowPopup) {
        this.isShow = isShowPopup;
      },
    },
    options() {
      return {
        respond: ["Approve", "Reject"],
      };
    },
  },
  methods: {
    submit() {
      if (this.modalType == "respond") {
        !this.response ? (this.showError = true) : (this.showError = false);
        if (this.showError) return;
        let payload = {
          activeStatus: this.response,
          comments: this.comments,
        };
        this.modalCallBack("Save", payload);
      } else if (this.modalType == "newApartment") {
        !this.apartment_name
          ? (this.showError = true)
          : (this.showError = false);
        if (this.showError) return;
        let payload = {
          apartment_name: this.apartment_name,
          description: this.description,
        };
        this.modalCallBack("Save", payload);
      }
    },
    clearFields() {
      this.response = "";
      this.comments = "";
    },
  },
};
</script>
<style scoped>
.err_msg {
  color: red;
  text-align: center;
}
</style>
