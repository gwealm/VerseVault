import { MainNav } from "@/components/nav/main-nav";
import { Suspense } from "react";

type PageProps = {
    searchParams: { [key: string]: string | string[] | undefined };
};

async function sleep(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

async function findTracksByQuery(query: string) {
    await sleep(5000);
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
                <MainNav />
                <main className="flex min-h-screen flex-col items-center justify-between p-24">
                    <h1>My Page</h1>
                </main>
            </>
        );
    // return to this page ut returns an error in red

    const searchResults = findTracksByQuery(q).then((tracks) => {
        return (
            <ul>
                {tracks.map((track) => {
                    return (
                        <li key={track.id}>
                            <h2>{track.title}</h2>
                            <p>
                                {track.artist} - {track.album}
                            </p>
                        </li>
                    );
                })}
            </ul>
        );
    });
    return (
        <>
            <MainNav />
            <main className="flex min-h-screen flex-col items-center justify-between p-24">
                <h1>My Page</h1>
                <Suspense fallback={<p>Loading...</p>}>
                    {searchResults}
                </Suspense>
            </main>
        </>
    );
}
