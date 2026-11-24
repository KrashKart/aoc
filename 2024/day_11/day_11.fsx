open System.Collections.Generic
open System.IO

let change (stone: int64) : int64 list = 
    match string stone with
    | "0" -> [1]
    | stone when stone.Length % 2 = 0 -> [stone[..stone.Length / 2 - 1] |> int64; stone[(stone.Length / 2)..] |> int64]
    | _ -> [(int64 stone) * 2024L]

let lines: string list = File.ReadLines("day_11/day_11.txt") |> List.ofSeq<string>
let line = List.ofArray (lines[0].Split(" "))

let mutable currRef, futureRef = new Dictionary<int64, int64>(), new Dictionary<int64, int64>()
let mutable (total1: int64), (total2: int64), (temp: int64)  = 0, 0, 0

for l: string in line do
    currRef.Add(int64 l, 1)

for i in 0..74 do
    if i = 25 then total1 <- Seq.sum currRef.Values

    futureRef <- new Dictionary<int64, int64>()
    for k: int64 in currRef.Keys do
        for newVal: int64 in change k do
            temp <- futureRef.GetValueOrDefault(newVal, 0) + currRef.Item k
            newVal |> futureRef.Remove |> ignore
            futureRef.Add(newVal, temp)

    currRef <- futureRef

total2 <- Seq.sum currRef.Values

printfn "Part 1: %i\nPart 2: %i" total1 total2