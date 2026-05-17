import api from "./axios";

export const login = async (data) => {
  return await api.post(
    "auth/login/",
    data
  );
};

export const getProfile = async () => {
  return await api.get(
    "auth/me/"
  );
};