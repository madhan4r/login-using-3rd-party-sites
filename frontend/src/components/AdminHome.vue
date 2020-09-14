<template>
  <div class="mt-3">
    <CContainer>
      <h4 class="text-center">DASHBOARD</h4>
      <CRow class="mt-4">
        <CCol col="12" sm="6">
          <CWidgetIcon
            :header="totalUserCount"
            text="Registered Users"
            color="primary"
          >
            <CIcon name="cil-user" />
          </CWidgetIcon>
        </CCol>
        <CCol col="12" sm="6">
          <CWidgetIcon
            :header="totalApartmentsCount"
            text="Registered Apartments"
            color="danger"
          >
            <CIcon name="cil-building" />
          </CWidgetIcon>
        </CCol>
      </CRow>
      <CTabs :fill="true" variant="pills" :fade="true" :active-tab="active_tab">
        <CTab title="Pending Apartments" class="mb-3">
          <CCardGroup class="content-center">
            <CCard
              class="m-3"
              style="min-width: 300px; max-width: 300px;"
              v-for="apartment in pendingApartments"
              :key="apartment.apartment_id"
              ><div class="p-3">
                <p>
                  <strong> Apartment Name :</strong>
                  {{ apartment.apartment_name.toUpperCase() }}
                </p>
                <p>
                  <strong>Description : </strong
                  >{{ apartment.description ? apartment.description : "--" }}
                </p>
                <p>
                  <strong> Active Status :</strong>
                  {{ apartment.activeStatus }}
                </p>
                <p><strong>Created by:</strong> {{ apartment.created_by_name }}</p>
                <p><strong>Created on:</strong> {{ apartment.created_on }}</p>
                <CRow class="justify-content-center">
                  <CButton
                    color="primary"
                    @click="respond(apartment.apartment_id)"
                    >Respond</CButton
                  >
                </CRow>
              </div>
            </CCard>
          </CCardGroup>
          <div class="mt-3" v-if="!pendingApartments.length">
            <h3 class="text-center">No Apartments Found</h3>
          </div>
        </CTab>
        <CTab title="Active Apartments">
          <CRow class="justify-content-center">
            <CInput class="ml-3" style="width:80%" v-model="searchTerm" />
            <CButton
              class="btn btn-primary small ml-3"
              style="max-height: 33px;"
              @click="searchFilter()"
              >Search</CButton
            >
          </CRow>
          <CCardGroup v-if="activeApartments" class="content-center">
            <CCard
              class="m-3"
              style="min-width: 300px; max-width: 300px;;"
              v-for="apartment in filteredApartments"
              :key="apartment.apartment_id"
              ><div class="p-3">
                <p>
                  <strong> Apartment Name :</strong>
                  {{ apartment.apartment_name.toUpperCase() }}
                </p>
                <p>
                  <strong>Description : </strong
                  >{{ apartment.description ? apartment.description : "--" }}
                </p>
                <p>
                  <strong> Active Status :</strong>
                  {{ apartment.activeStatus == 'Approve' ? 'Approved' : '--' }}
                </p>
                <p><strong>Created by:</strong> {{ apartment.created_by_name }}</p>
                <p>
                  <strong>Reviewed on:</strong> {{ apartment.activated_on }}
                </p>
                <p>
                  <strong>Joined Users: </strong
                  >{{ apartment.joinedUsers.length }}
                </p>
                <CRow class="justify-content-center">
                  <CButton
                    color="primary"
                    @click="respond(apartment.apartment_id)"
                    >Deactivate</CButton
                  >
                </CRow>
              </div>
            </CCard>
          </CCardGroup>
          <div class="mt-3" v-if="!filteredApartments.length">
            <h3 class="text-center">No Apartments Found</h3>
            <CRow class="content-center">
              <CButton class="mt-2 btn-primary" @click="newApartment">
                Want To Create New Apartment?
              </CButton>
            </CRow>
          </div>
        </CTab>
        <CTab title="Rejected Apartments">
          <CCardGroup class="content-center">
            <CCard
              class="m-3"
              style="min-width: 300px; max-width: 300px;;"
              v-for="apartment in rejectedApartments"
              :key="apartment.apartment_id"
              ><div class="p-3">
                <p>
                  <strong> Apartment Name :</strong>
                  {{ apartment.apartment_name.toUpperCase() }}
                </p>
                <p>
                  <strong>Description : </strong
                  >{{ apartment.description ? apartment.description : "--" }}
                </p>
                <p>
                  <strong> Active Status :</strong>
                  {{ apartment.activeStatus.toUpperCase() }}
                </p>
                <p><strong>Created by:</strong> {{ apartment.created_by_name }}</p>
                <p>
                  <strong>Reviewed on:</strong> {{ apartment.activated_on }}
                </p>
                <CRow class="justify-content-center">
                  <CButton
                    color="primary"
                    @click="respond(apartment.apartment_id)"
                    >Approve</CButton
                  >
                </CRow>
              </div>
            </CCard>
          </CCardGroup>
          <div class="mt-3" v-if="!rejectedApartments.length">
            <h3 class="text-center">No Apartments Found</h3>
          </div>
        </CTab>
      </CTabs>
    </CContainer>
    <PopupModal
      :modalTitle="popupModal.modalTitle"
      :modalColor="popupModal.modalColor"
      :modalContent="popupModal.modalContent"
      :isShowPopup="popupModal.isShowPopup"
      :modalCallBack="modalCallBack"
      :closeOnBackdrop="true"
      :modalType="popupModal.modalType"
    />
  </div>
</template>

<script>
import services from "@/services/services";
import PopupModal from "@/components/PopupModal";

export default {
  name: "AdminHome",
  props: ["userProfile"],
  components: {
    PopupModal,
  },
  data() {
    return {
      totalUsers: [],
      totalUserCount: "0",
      totalApartments: [],
      totalApartmentsCount: "0",
      selectedApartment: "",
      filteredApartments: [],
      popupModal: {
        modalTitle: "",
        modalColor: "",
        modalContent: "",
        isShowPopup: false,
        modalType: "",
      },
      searchTerm: "",
      active_tab: 1,
    };
  },
  computed: {
    pendingApartments() {
      return this.totalApartments
        ? this.totalApartments.filter((val) => {
            return val.activeStatus == "Under Review";
          })
        : [];
    },
    activeApartments() {
      return this.totalApartments
        ? this.totalApartments.filter((val) => {
            return val.activeStatus == "Approve";
          })
        : [];
    },
    rejectedApartments() {
      return this.totalApartments
        ? this.totalApartments.filter((val) => {
            return val.activeStatus == "Reject";
          })
        : [];
    },
  },
  watch: {
    activeApartments() {
      this.filteredApartments = this.activeApartments;
    },
    pendingApartments() {
      this.pendingApartments.length ? (this.active_tab = 0) : null;
    },
  },
  mounted() {
    this.getAllApartments();
    this.getAllUsers();
  },
  methods: {
    getAllApartments() {
      return services.getAllApartments().then((res) => {
        this.totalApartments = res.data;
        this.totalApartmentsCount = res.data.length.toString();
      });
    },
    getAllUsers() {
      return services.getAllUsers().then((res) => {
        this.totalUsers = res.data;
        let count = res.data.length - 1;
        this.totalUserCount = count.toString();
      });
    },
    searchFilter() {
      if (this.searchTerm) {
        this.filteredApartments = this.activeApartments.filter((val) => {
          return val.apartment_name.includes(this.searchTerm);
        });
      } else {
        this.filteredApartments = this.activeApartments;
      }
    },
    respond(id) {
      this.selectedApartment = id;
      this.popupModal.modalTitle = "Confirmation Modal";
      this.popupModal.modalColor = "primary";
      this.popupModal.modalContent =
        "Please select any option from respond dropdown and save!...";
      this.popupModal.modalType = "respond";
      this.popupModal.isShowPopup = true;
    },
    newApartment() {
      this.popupModal.modalTitle = "New Apartment";
      this.popupModal.modalColor = "primary";
      this.popupModal.modalContent = "Please enter your Apartment Name...!";
      this.popupModal.modalType = "newApartment";
      this.popupModal.isShowPopup = true;
    },
    modalCallBack(action, value) {
      this.popupModal.isShowPopup = false;
      if (action == "Save") {
        let payload = value;
        if (this.popupModal.modalType == "respond") {
          let apartment_id = this.selectedApartment;
          return services.updateApartment(apartment_id, payload).then(() => {
            this.getAllApartments();
            this.$emit("toaster", "Apartment updated successfully");
          });
        } else if (this.popupModal.modalType == "newApartment") {
          payload.created_by = this.userProfile.user_id;
          payload.created_by_name = this.userProfile.user_name;
          return services.createApartment(payload).then(() => {
            this.getAllApartments();
            this.$emit("toaster", "Apartment created successfully");
          });
        }
      }
    },
  },
};
</script>
