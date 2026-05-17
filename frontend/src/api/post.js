import api from "./axios";

export const getPosts = async () => {
  return await api.get("posts/");
};

export const createPost = async (data) => {
  return await api.post(
    "posts/",
    data
  );
};