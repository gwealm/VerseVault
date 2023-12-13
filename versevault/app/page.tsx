import { SearchBox } from "@/components/search-box/search-box";

async function search(formData: FormData) {

  const q = formData.get("q");
  if (!q || typeof q !== "string") {
    return { success: false, error: "Invalid search query" };
  }
}

async function findCores() {

  const res = await fetch(`http://127.0.0.1:5000/cores`)
  const cores = await res.json()

  const names = Object.keys(cores.status)

  return names
}

export default async function Home() {

  const cores = await findCores()

  return (
    <>
      <main className="flex flex-col p-24">
        <SearchBox cores={cores}  />
      </main>
    </>
  );
}
