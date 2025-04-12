import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";
import { api } from "~/api";

export function meta() {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  const { data } = api.useQuery("get", "/api/v1/hello");
  const { mutate } = api.useMutation("post", "/api/v1/login/");
  return (
    <>
      <div>
        {data?.message}
        <input type="text" />
        <input type="password" />
        <button
          type="button"
          onClick={() =>
            mutate({
              body: {
                username: "test",
                password: "test",
              },
            })
          }
        >
          Login
        </button>
      </div>
      <Welcome />
    </>
  );
}
