"use client";

import Link from "next/link";
import React, { useState } from "react";

type SearchBarProps = {
    core: string;
};

export const SearchBar = ({ core }: SearchBarProps) => {
    const [query, setQuery] = useState("");

    return (
        <>
            <div className="flex mt-20 flex-col items-center justify-center">
                <div>
                    <h1 className="font-sans text-6xl font-bold text-center">
                        VerseVault
                    </h1>
                </div>
                <div className="md:w-[584px] mx-auto mt-7 flex w-[92%] items-center rounded-full border hover:shadow-md">
                    <div className="pl-5">
                        <Link href={`/search/?core=tracks_semantic&q=${query}`}>
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                className="h-6 w-6 text-gray-400"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                                strokeWidth="2"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                                />
                            </svg>
                        </Link>
                    </div>
                    <input
                        name="query"
                        id="query"
                        value={query}
                        type="text"
                        className="w-full bg-transparent rounded-full py-[14px] pl-4 outline-none"
                        onChange={(e) => setQuery(e.target.value)}
                    />
                </div>
            </div>
        </>
    );
};
