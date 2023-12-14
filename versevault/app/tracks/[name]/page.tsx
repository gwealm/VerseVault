type PageProps = {
    searchParams: { core: string}
    params: { name: string }
}

type TrackDataType = {
    id: string,
    name: string,
    artist: string,
    genres: string[],
    lyrics: LyricsSectionType[]
    'album.name': string
}

type LyricsSectionType = {
    title: string,
    content: string
}

export default async function Page({ searchParams, params }: PageProps) {

    const { core } = searchParams
    const { name } = params

    const response = await fetch(`http://127.0.0.1:5000/${core}/tracks/${name}`, { cache: "no-cache" })

    const track = await response.json()
    const trackData: TrackDataType = track.response.docs[0]
    const lyricsSection = trackData.lyrics

    console.log(trackData)
    return (
        <>
            <div className="flex flex-col justify-center align-middle">
                <span className="flex justify-center text-2xl font-semibold">{trackData.name} - {trackData.artist}</span>
                <span className="flex justify-center text-2xl font-semibold">{trackData['album.name']}</span>
                <div className="m-2 flex gap-2 flex-col">
                    {
                        lyricsSection.map((section) => (
                            <div className="flex flex-col justify-center bg-gray-400 rounded-md p-2">
                                <span className="flex justify-center">{section.title}</span>
                                <span className="flex">{section.content}</span>
                            </div>
                        ))
                    }
                </div>
            </div>
        </>
    )

}