#include "hooks.h"

#include "MinHook/MinHook.h"
#include "patternscan.h"

#include <stdio.h>


inventory_func_t original_inventory = nullptr;



bool hooked_inventory(
    uint64_t param1,
    uint32_t itemID,
    uint32_t amount,
    uint32_t param4
)
{
    printf(
        "[Inventory] object=%llX item=%u amount=%u param4=%u\n",
        param1,
        itemID,
        amount,
        param4
    );

    fflush(stdout);


    return original_inventory(
        param1,
        itemID,
        amount,
        param4
    );
}



bool HookInventory()
{
    printf("[Inventory] Searching...\n");


    /*
        First bytes from:

        142155820

        44 89 4C 24 20
        44 89 44 24 18
        89 54 24 10
        48 89 4C 24 08
    */


    uintptr_t address = PatternScan(
        "44 89 4C 24 20 44 89 44 24 18 89 54 24 10 48 89 4C 24 08"
    );


    if(!address)
    {
        printf(
            "[Inventory] Pattern not found\n"
        );

        return false;
    }


    printf(
        "[Inventory] Found at %p\n",
        (void*)address
    );


    if(
        MH_CreateHook(
            (LPVOID)address,
            &hooked_inventory,
            (LPVOID*)&original_inventory
        )
        != MH_OK
    )
    {
        printf(
            "[Inventory] CreateHook failed\n"
        );

        return false;
    }


    if(
        MH_EnableHook(
            (LPVOID)address
        )
        != MH_OK
    )
    {
        printf(
            "[Inventory] EnableHook failed\n"
        );

        return false;
    }


    printf(
        "[Inventory] Hook active\n"
    );


    return true;
}