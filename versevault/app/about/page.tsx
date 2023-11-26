import Image from "next/image";
import { Input } from "@/components/ui/input";
import { MainNav } from "@/components/nav/main-nav";
import { Button } from "@/components/ui/button";
import { Search } from "@/components/search/search";
import { ParallaxGlare } from "@/components/utils/parallax-glare";

async function search(formData: FormData) {
    "use server";

    const q = formData.get("q");
    if (!q || typeof q !== "string") {
        return { success: false, error: "Invalid search query" };
    }
}

export default function Page() {
    const developers = [
        {
            name: "André Lima",
            linkedin: "https://www.linkedin.com/in/limwa/",
            instagram: "https://www.instagram.com/limaaaaaaaa_/",
            github: "",
            website: "https://www.limwa.pt",
            imagePath: "/lima.jpg",
        },
        {
            name: "Guilherme Almeida",
            linkedin: "https://www.linkedin.com/in/gui1612/",
            instagram: "https://www.instagram.com/gui.1612/",
            github: "https://github.com/gui1612",
            website: "https://www.gui1612.com/",
            imagePath: "/gui.jpg",
        },
        {
            name: "Jorge Sousa",
            linkedin: "https://www.linkedin.com/in/jorge-sousa-036761208/",
            instagram: "https://www.instagram.com/jorge_sousa02/",
            github: "https://github.com/jsousa02",
            imagePath: "/jorge.jpg",
        },
        {
            name: "José Castro",
            linkedin: "https://www.linkedin.com/in/zmcastro/",
            instagram: "https://www.instagram.com/zcastro_/",
            imagePath: "/ze.jpg",
        },
    ];

    return (
        <>
            <main>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 p-8 rounded ">
                    <div>
                        <h1 className="text-3xl font-bold mb-6 text-center">
                            About Us
                        </h1>
                        <div className="text-left text-lg">
                            <p className="text-gray-400">
                                We are a team of four students pursuing of
                                Informatics Engineering at FEUP (Faculdade de
                                Engenharia da Universidade do Porto). Our
                                passion for music and technology has brought us
                                together to develop a Lyric-based Search Engine
                                for finding songs.
                            </p>
                            <p className="text-gray-400 mt-8">
                                Our project aims to aggregate various metadata
                                regarding musical content, providing a
                                centralized and rich data source for music
                                enthusiasts. By allowing text-based querying
                                with the aid of context-sensitive filters, our
                                search engine makes it easy to explore the vast
                                and unexplored world of lyrical and structural
                                musical data.
                            </p>
                            <p className="text-gray-400 mt-8">
                                In its final stage, our search engine will be a
                                fun and interactive way to interact and perceive
                                music production and its history. Join us on
                                this musical journey!
                            </p>
                        </div>
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold mb-4 text-center">
                            Developers
                        </h1>

                        <div className="flex flex-wrap justify-center">
                            {developers.map((developer, index) => (
                                <ParallaxGlare
                                    key={index}
                                    data={developer}
                                    border={true}
                                />
                            ))}
                        </div>
                    </div>
                </div>
            </main>
        </>
    );
}
