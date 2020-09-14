import axios from "axios"

const services = {
    access_token: (payload) => { return axios.post(`http://127.0.0.1:8000/user/access-token`, payload) },
    loginWith: (login_type, payload) => { return axios.post(`http://127.0.0.1:8000/${login_type}/user/access-token`, payload) },
    createUser: (payload) => { return axios.post(`http://127.0.0.1:8000/user/create`, payload) },
    updateUser: (user_id, payload) => { return axios.put(`http://127.0.0.1:8000/user/${user_id}/update`, payload) },
    getByID: (user_id) => { return axios.get(`http://127.0.0.1:8000/user/${user_id}`) },
    getAllUsers: () => { return axios.get(`http://127.0.0.1:8000/users/?limit=1000`) },
    fbUserData: (access_token) => { return axios.get(`https://graph.facebook.com/v8.0/me?fields=id%2Cname&access_token=${access_token}`) },
    createApartment: (payload) => { return axios.post(`http://127.0.0.1:8000/apartment/create`, payload) },
    getAllApartments: () => { return axios.get(`http://127.0.0.1:8000/apartments/?limit=1000`) },
    updateApartment: (apartment_id, payload) => { return axios.put(`http://127.0.0.1:8000/apartment/${apartment_id}/update`, payload) },
    joinApartment: (payload) => { return axios.post(`http://127.0.0.1:8000/apartment/join`, payload) },
    updateJoinApartment: (joinApartment_id, payload) => { return axios.put(`http://127.0.0.1:8000/apartment/join/${joinApartment_id}/update`, payload) }
};

export default services