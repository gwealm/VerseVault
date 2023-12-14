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
            <select name="cores" id="cores" defaultValue={selectedCore} onChange={(e) => { setSelectedCore(e.target.value) }}>
                {
                    cores.map((core, index) => (
                        <option key={index} value={core}>{core}</option>
                    ))
                }
            </select>
        </>
    )
}