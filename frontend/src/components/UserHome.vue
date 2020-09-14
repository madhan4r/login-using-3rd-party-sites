<template>
  <div>
    <div class="mt-3">
      <CContainer>
        <h4 class="text-center">DASHBOARD</h4>
        <CTabs :fill="true" variant="pills" :fade="true" :active-tab="0">
          <CTab title="My Apartments" class="mb-3"
            ><CCardGroup class="content-center">
              <CCard
                class="m-3"
                style="min-width: 300px; max-width: 300px"
                v-for="apartment in myApartments"
                :key="apartment.apartment_id"
                ><div class="p-3">
                  <p>
                    <strong> Apartment Name :</strong>
                    {{ apartment.apartment_name.toUpperCase() }}
                  </p>
                  <p>
                    <strong>Description : </strong>{{ apartment.description }}
                  </p>
                  <p style="color:red;">
                    <strong> Active Status :</strong>
                    {{
                      apartment.activeStatus == "Approve"
                        ? "Approved"
                        : apartment.activeStatus
                    }}
                  </p>
                  <p>
                    <strong>Activated On :</strong> {{ apartment.activated_on }}
                  </p>
                  <p>
                    <strong>joined Users :</strong> {{ apartment.joinedUsers }}
                  </p>
                  <p><strong>Created on:</strong> {{ apartment.created_on }}</p>
                </div>
              </CCard>
            </CCardGroup>
            <div class="mt-3" v-if="!myApartments.length">
              <h3 class="text-center">No Apartments Found</h3>
            </div></CTab
          >
          <CTab title="Pending Request" class="mb-3">
            <CCardGroup
              class="content-center"
              v-if="pendingRequest.pending"
            >
              <CCard
                class="m-3"
                style="min-width: 300px; max-width: 300px"
                v-for="apartment in pendingRequest.active"
                :key="apartment.apartment_id"
                ><div class="p-3">
                  <p>
                    <strong> Apartment Name :</strong>
                    {{ apartment.apartment_name.toUpperCase() }}
                  </p>
                  <p>
                    <strong>Description : </strong>{{ apartment.description }}
                  </p>
                  <p><strong>Requested Users</strong></p>
                  <CRow class="content-center">
                    <div
                      v-for="(user, Index) in apartment.joinedUsers"
                      :key="Index"
                    >
                      <div v-if="user.activeStatus == 'Under Review'">
                        <p><strong>User Name: </strong>{{ user.user_name }}</p>
                        <p>
                          <strong>Requested On: </strong>{{ user.joined_on }}
                        </p>
                        <CButton
                          @click="respond(user.joinApartment_id)"
                          color="primary"
                        >
                          Respond
                        </CButton>
                      </div>
                    </div>
                  </CRow>
                </div>
              </CCard>
            </CCardGroup>
            <div class="mt-3" v-if="!pendingRequest.pending">
              <h3 class="text-center">No Apartments Found</h3>
            </div>
          </CTab>
          <CTab title="All Apartments" class="mb-3">
            <CRow class="justify-content-center">
              <CInput class="ml-3" style="width:80%" v-model="searchTerm" />
              <CButton
                class="btn btn-primary small ml-3"
                style="max-height: 33px;"
                @click="searchFilter()"
                >Search</CButton
              >
            </CRow>
            <CCardGroup v-if="allApartments" class="content-center">
              <CCard
                class="m-3"
                style="min-width: 300px; max-width: 300px"
                v-for="apartment in filteredApartments"
                :key="apartment.apartment_id"
                ><div class="p-3">
                  <p>
                    <strong> Apartment Name :</strong>
                    {{ apartment.apartment_name.toUpperCase() }}
                  </p>
                  <p>
                    <strong> description :</strong>
                    {{ apartment.description ? apartment.description : "--" }}
                  </p>
                  <p>
                    <strong>Joined Users :</strong
                    >{{ apartment.joinedUsers.length }}
                  </p>
                  <CRow class="justify-content-center">
                    <CButton
                      class="col-6"
                      :disabled="checkMe(apartment.joinedUsers)"
                      color="primary"
                      @click="joinApartment(apartment.apartment_id)"
                      >Join</CButton
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
          <CTab title="Joined Apartments" class="mb-3">
            <CCardGroup v-if="joinedApartments.length" class="content-center">
              <CCard
                class="m-3"
                style="min-width:30px; max-width: 400px;"
                v-for="apartment in joinedApartments"
                :key="apartment.apartment_id"
                ><div class="p-3">
                  <p>
                    <strong> Apartment Name :</strong>
                    {{ apartment.apartment_name.toUpperCase() }}
                  </p>
                  <p>
                    <strong>Joined on :</strong> {{ apartment.reviewed_on }}
                  </p>
                  <p>
                    <strong>Joined Users : </strong>
                    {{ apartment.joinedUsers.length }}
                  </p>
                </div>
              </CCard>
            </CCardGroup>
            <div class="mt-3" v-if="!joinedApartments.length">
              <h3 class="text-center">No Apartments Joined</h3>
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
  </div>
</template>

<script>
import services from "@/services/services";
import PopupModal from "@/components/PopupModal";

export default {
  name: "UserHome",
  props: ["userProfile"],
  components: {
    PopupModal,
  },
  data() {
    return {
      userCreatedApartments: [],
      totalApartments: [],
      filteredApartments: [],
      popupModal: {
        modalTitle: "",
        modalColor: "",
        modalContent: "",
        isShowPopup: false,
        modalType: "",
      },
      searchTerm: "",
      selectedJoinApartment: 0,
    };
  },
  computed: {
    myApartments() {
      return this.userCreatedApartments
        ? this.userCreatedApartments.map((val) => {
            let data = {
              apartment_id: val.apartment_id,
              apartment_name: val.apartment_name,
              description: val.description ? val.description : "--",
              created_on: val.created_on,
              activeStatus: val.activeStatus,
              activated_on: val.activated_on ? val.activated_on : "--",
              joinedUsers: val.joinedUsers.length,
            };
            return data;
          })
        : [];
    },
    pendingRequest() {
      let active = this.userCreatedApartments
        ? this.userCreatedApartments
            .filter((val) => {
              return val.activeStatus == "Approve";
            })
            .map((val) => {
              let data = {
                apartment_id: val.apartment_id,
                apartment_name: val.apartment_name,
                description: val.description ? val.description : "--",
                joinedUsers: val.joinedUsers,
              };
              return data;
            })
        : [];
      let pending = false;
      active
        ? active.filter((val) => {
            val.joinedUsers.filter((value) => {
              pending = value.activeStatus == "Under Review" ? true : pending;
            });
          })
        : [];
      return active && pending ? { active, pending } : [];
    },
    allApartments() {
      return this.totalApartments
        ? this.totalApartments.filter((val) => {
            return val.activeStatus == "Approve";
          })
        : [];
    },
    joinedApartments() {
      let joined = this.userProfile.joinedApartments
        ? this.userProfile.joinedApartments.filter((val) => {
            return val.activeStatus == "Approve";
          })
        : [];
      if (!joined) {
        return [];
      }
      return joined.map((val) => {
        if (!this.totalApartments) {
          return [];
        }
        let getApartment = this.totalApartments.filter((value) => {
          return value.apartment_id == val.apartment_id;
        });
        return {
          apartment_name: getApartment[0].apartment_name,
          joinedUsers: getApartment[0].joinedUsers,
          reviewed_on: val.reviewed_on,
        };
      });
    },
  },
  watch: {
    allApartments() {
      this.filteredApartments = this.allApartments ? this.allApartments : [];
    },
    userProfile() {
      this.userCreatedApartments = this.userProfile.createdApartments;
    },
  },
  mounted() {
    this.getAllApartments();
  },
  methods: {
    getAllApartments() {
      return services.getAllApartments().then((res) => {
        this.totalApartments = res.data;
      });
    },
    searchFilter() {
      if (this.searchTerm) {
        this.filteredApartments = this.allApartments.filter((val) => {
          return val.apartment_name.includes(this.searchTerm);
        });
      } else {
        this.filteredApartments = this.activeApartments;
      }
    },
    checkMe(data) {
      return data.some((val) => val.user_id == this.userProfile.user_id);
    },
    joinApartment(apartment_id) {
      let payload = {
        apartment_id: apartment_id,
        user_id: this.userProfile.user_id,
        user_name: this.userProfile.user_name,
      };
      services.joinApartment(payload).then(() => {
        this.$emit("getMe", this.userProfile.user_id);
        this.getAllApartments();
        this.$emit("toaster", "Joined successfully");
      });
    },
    respond(id) {
      this.selectedJoinApartment = id;
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
          let joinApartment_id = this.selectedJoinApartment;
          return services
            .updateJoinApartment(joinApartment_id, payload)
            .then(() => {
              this.$emit("getMe", this.userProfile.user_id);
              this.getAllApartments();
              this.$emit("toaster", "Apartment updated successfully");
            });
        } else if (this.popupModal.modalType == "newApartment") {
          payload.created_by = this.userProfile.user_id;
          payload.created_by_name = this.userProfile.user_name;
          return services
            .createApartment(payload)
            .then(() => {
              this.$emit("getMe", this.userProfile.user_id);
              this.getAllApartments();
              this.$emit("toaster", "Apartment created successfully");
            })
            .catch((err) => {
              this.$emit("toaster", err.response.data.detail);
            });
        }
      }
    },
  },
};
</script>
