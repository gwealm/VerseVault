"use client"

import { SearchBar } from "@/components/search/search-bar";
import { useState } from "react";

type SearchBoxProps = {
    cores: string[]
}

export function SearchBox({cores}: SearchBoxProps) {
    let [core, setCore] = useState("");  

    core = cores[0]

    return (
        <>
            <SearchBar core={core} /> 
            <select name="cores" id="cores" onChange={(e) => {
                
                console.log("Target core:\n")
                console.log(e.target.value)
                console.log(core)
                setCore(e.target.value)
            }}>
            {
            cores.map((core, index) => (
                <option key={index} value={core}>{core}</option>
            ))
            }
        </select>
        </>
    )
}