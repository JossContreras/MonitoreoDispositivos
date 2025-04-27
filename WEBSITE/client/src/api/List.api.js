import axios from 'axios';

export const GetAllList = () => {
   return axios.get('http://127.0.0.1:8000/inventario/')
}

export const GetAllUbi = () => {
   return axios.get('http://127.0.0.1:8000/ubicacion/')
}

export const GetDisp = (id) => {
   return axios.get(`http://127.0.0.1:8000/inventario/${id}/`)
}

export const createDisp = (Disp) => {
   return axios.post('http://127.0.0.1:8000/inventario/', Disp);
};

export const createLocate = (Ubi) => {
   return axios.post('http://127.0.0.1:8000/ubicacion/', Ubi);
};

export const deleteDisp = (id) => {
   return axios.delete(`http://127.0.0.1:8000/inventario/${id}/`)
};

export const updateDisp = (id, Disp) => {
   return axios.put(`http://127.0.0.1:8000/inventario/${id}/`,Disp)
};