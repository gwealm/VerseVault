import { MainNav } from "@/components/nav/main-nav";
import { Suspense } from "react";

type PageProps = {
    searchParams: { [key: string]: string | string[] | undefined };
};

async function sleep(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

async function findTracksByQuery(query: string) {
    "use server"

    await sleep(1000);

    const res = await fetch('http://127.0.0.1:5000', {method: 'get'});
    console.log(res)
    return await res.json()

    return [
        {
            id: "1",
            title: "My Track",
            artist: "My Artist",
            album: "My Album",
        },
        {
            id: "2",
            title: "My Track 2",
            artist: "My Artist 2",
            album: "My Album 2",
        },
        {
            id: "3",
            title: "My Track 3",
            artist: "My Artist 3",
            album: "My Album 3",
        },
    ];
}

export default function Page({ searchParams }: PageProps) {
    const { q } = searchParams;

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

    const searchResults = findTracksByQuery(q).then((tracks) => {
        return (
            <ul>
                {tracks}
            </ul>
        );
    });
    return (
        <>
            <main className="flex min-h-screen flex-col items-center justify-between p-24">
                <h1>My Page</h1>
                <Suspense fallback={<p>Loading...</p>}>
                    {searchResults}
                </Suspense>
            </main>
        </>
    );
}
