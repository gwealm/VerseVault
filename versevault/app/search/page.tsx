import { Suspense } from "react";

type PageProps = {
    searchParams: { [key: string]: string | string[] | undefined };
};

type SolrResponseProps = {
    docs: [],
    maxScore: number,
    numFound: number,
    numFoundExact: boolean,
    start: number,
}

type DocumentProps = {
    artist: string,
    id: string,
    lyrics: [],
    name: string,
    score: number,
}

async function findTracksByQuery(query: string) {
    "use server"

    const res = await fetch(`http://127.0.0.1:5000?q=${query}`, {method: 'get'});
    const r = await res.json()

    return r
}

export default function Page({ searchParams }: PageProps) {
    const { q } = searchParams;
    console.log(q)

    // TODO: Implement this
    if (!q || typeof q !== "string")
        return (
            <>
                <main className="flex min-h-screen flex-col items-center justify-between p-24">
                    <h1>My Page</h1>
                </main>
            </>
        );
    // return to this page ut returns an error in red
    const searchResults = findTracksByQuery(q).then((res) => {
        const response: SolrResponseProps = res.response

        return (
            <ul>
                {
                    response.docs.map((el: DocumentProps, index: number) => (
                        <li className="flex flex-row gap-2 justify-between" key={index}>
                            <span>{el.artist}</span>
                            <span>{el.score}</span>
                        </li>
                    ))
                }
            </ul>
        );
    })
        
    return (
        <>
            <main className="flex min-h-screen flex-col items-center mt-1 gap-2">
                <h1 className="text-xl flex">{`Results for: ${q}`}</h1>
                <Suspense fallback={<p>Loading...</p>}>
                    <div className="flex">
                        {searchResults}
                    </div>
                </Suspense>
            </main>
        </>
    );
}
