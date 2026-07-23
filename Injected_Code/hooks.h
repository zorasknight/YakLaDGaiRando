#pragma once
#include <Windows.h>
#include <cstdint>


typedef bool(*inventory_func_t)(
    uint64_t,
    uint32_t,
    uint32_t,
    uint32_t
);


extern inventory_func_t original_inventory;


bool HookInventory();