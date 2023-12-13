import Image from "next/image";
import Link from "next/link";
import { redirect } from "next/navigation";
import { Suspense } from "react";

type PageProps = {
    searchParams: { [key: string]: string | string[] | undefined };
};

type SolrResponseProps = {
    docs: DocumentProps[],
    maxScore: number,
    numFound: number,
    numFoundExact: boolean,
    start: number,
}

type DocumentProps = {
    artist: string,
    id: string,
    "album.image": string,
    lyrics: [],
    name: string,
    score: number,
}

async function findTracksByQuery(query: string, core: string) {
    "use server"

    const res = await fetch(`http://127.0.0.1:5000/${core}?q=${query}`, {method: 'get', cache: 'no-cache'});
    const r = await res.json()

    return r
}

export default function Page({ searchParams }: PageProps) {
    const { q } = searchParams;
    const { core } = searchParams;
    console.log(core)

    if (!q || typeof q !== "string")
        redirect("/");

    // return to this page ut returns an error in red
    const searchResults = findTracksByQuery(q, core).then((res) => {
        const response: SolrResponseProps = res.response

        return (
            <ul className="flex flex-col gap-4 w-full p-4">
                {
                    response.docs.map((el: DocumentProps, index: number) => (
                        <li key={index}>
                            <Link href="/tracks/gjkfhktgh" className="block bg-neutral-800 flex gap-2 h-32">
                                <div className="grow-0">
                                    <Image src={el["album.image"] ?? "https://avatars.githubusercontent.com/t/8605584?s=116&v=4"} width={128} height={128} alt="" className="h-full aspect-square object-cover" />
                                </div>
                                <div className="grow p-2">
                                    <p className="font-bold text-lg">{el.name}</p>
                                    <p className="text-neutral-400">{el.artist}</p>
                             </div>
                             </Link>
                        </li>
                    ))
                }
            </ul>
        );
    })
        
    return (
        <>
            <main className="flex min-h-screen flex-col items-center mt-1 gap-2">
                <h1 className="text-xl flex w-full">{`Results for: ${q}`}</h1>
                <Suspense fallback={<p>Loading...</p>}>
                    {searchResults}
                </Suspense>
            </main>
        </>
    );
}
