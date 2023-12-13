"use client"

import { SearchBar } from "@/components/search/search-bar";
import { useState } from "react";

type SearchBoxProps = {
    cores: string[]
}

export function SearchBox({cores}: SearchBoxProps) {
    const [core, setCore] = useState("");  

    return (
        <>
            <SearchBar core={core} /> 
            <select name="cores" id="cores" onChange={(e) => setCore(e.target.value)}>
            {
            cores.map((core, index) => (
                <option key={index} value={core}>{core}</option>
            ))
            }
        </select>
        </>
    )
}