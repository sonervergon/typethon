import type { Route } from "./+types/home";
import { Welcome } from "../welcome/welcome";
import { api } from "~/api";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export default function Home() {
  const { data } = api.useQuery("get", "/api/v1/hello");
  console.log(data);
  return (
    <>
      <div>{data?.message}</div>
      <Welcome />
    </>
  );
}
