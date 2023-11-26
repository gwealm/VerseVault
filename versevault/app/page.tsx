import { SearchBar } from "@/components/search/search-bar";

async function search(formData: FormData) {
  "use server";

  const q = formData.get("q");
  if (!q || typeof q !== "string") {
    return { success: false, error: "Invalid search query" };
  }
}


export default function Home() {

  return (
    <>
      <main className="flex flex-col p-24">
        <SearchBar />
      </main>
    </>
  );
}
