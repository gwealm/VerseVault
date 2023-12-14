"use client"

import { SearchBar } from "@/components/search/search-bar";
import { useState } from "react";

type SearchBoxProps = {
    cores: string[]
}

export function SearchBox({cores}: SearchBoxProps) {
    let [selectedCore, setSelectedCore] = useState(cores[0]);  

    return (
        <>
            <SearchBar core={selectedCore} /> 
        </>
    )
}