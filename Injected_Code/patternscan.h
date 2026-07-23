#pragma once

#include <Windows.h>
#include <vector>
#include <string>
#include <cstdint>
#include <cstring>
#include <cstdlib>


inline std::vector<int> pattern_to_bytes(const char* pattern)
{
    std::vector<int> bytes;

    auto start = const_cast<char*>(pattern);
    auto end = start + strlen(pattern);

    for (auto current = start; current < end; ++current)
    {
        if (*current == '?')
        {
            ++current;

            if (*current == '?')
                ++current;

            bytes.push_back(-1);
        }
        else
        {
            bytes.push_back(strtoul(current, &current, 16));
        }
    }

    return bytes;
}


inline uintptr_t PatternScan(
    uintptr_t module,
    const char* signature)
{
    auto dosHeader =
        (PIMAGE_DOS_HEADER)module;

    auto ntHeaders =
        (PIMAGE_NT_HEADERS)
        (module + dosHeader->e_lfanew);


    auto size =
        ntHeaders->OptionalHeader.SizeOfImage;


    auto patternBytes =
        pattern_to_bytes(signature);


    auto scanBytes =
        (uint8_t*)module;


    size_t s =
        patternBytes.size();


    for (size_t i = 0;
        i < size - s;
        i++)
    {
        bool found = true;


        for (size_t j = 0;
            j < s;
            j++)
        {
            if (scanBytes[i+j] != patternBytes[j]
                && patternBytes[j] != -1)
            {
                found = false;
                break;
            }
        }


        if (found)
            return (uintptr_t)&scanBytes[i];
    }


    return 0;
}


inline uintptr_t PatternScan(
    const char* signature)
{
    return PatternScan(
        (uintptr_t)GetModuleHandle(NULL),
        signature);
}