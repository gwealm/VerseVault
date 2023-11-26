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
        <div>
            <p className="text-3xl font-bold mb-6 ">
                How can I use VerseVault? 🤔
            </p>
            <p className="text-lg">
                Don't feel scared to use VerseVault, it's very simple! Just type in the search bar the verse you want like you would do in any other search engine of your choice to find and we will do the rest for you! 😁
            </p>
        </div>

        <div className="mt-20">
            <p className="text-3xl font-bold mb-6 ">
                But what if I am an experienced user? 😢
            </p>
            <p className="text-lg">
                Do not worry, we have you covered! You can use the advanced search queries and parameters to find the specific information you want as you will see in the following section! 😎
            </p>
        </div>

        <div className="mt-20">
            <p className="text-3xl font-bold mb-6 ">
                Query Examples ⚙️
            </p>

            <p className="text-2xl">
                1. Search for a specific verse:
            </p>
            <p className="text-lg">
                TODO....
            </p>
        </div>
        
      </main>
    </>
  );
}