#include <Windows.h>
#include <stdio.h>

#include "hooks.h"
#include "MinHook/MinHook.h"

#pragma comment(lib, "MinHook/MinHook.x64.lib")


HMODULE g_Module = nullptr;


DWORD WINAPI MainThread(HMODULE module)
{
    AllocConsole();

    FILE* fp;
    freopen_s(
        &fp,
        "CONOUT$",
        "w",
        stdout
    );


    printf("[InventoryMod] DLL loaded\n");
    fflush(stdout);


    // Give the game time to finish loading
    Sleep(3000);


    MH_STATUS status = MH_Initialize();

    if(status != MH_OK)
    {
        printf(
            "[InventoryMod] MinHook failed: %d\n",
            status
        );

        fflush(stdout);
        return 0;
    }


    printf("[InventoryMod] MinHook initialized\n");
    fflush(stdout);


    if(!HookInventory())
    {
        printf(
            "[InventoryMod] Inventory hook failed\n"
        );
    }
    else
    {
        printf(
            "[InventoryMod] Inventory hook installed\n"
        );
    }

    fflush(stdout);


    while(true)
    {
        Sleep(1000);
    }


    // Never reached currently
    MH_Uninitialize();

    FreeLibraryAndExitThread(
        module,
        0
    );

    return 0;
}



BOOL WINAPI DllMain(
    HMODULE hModule,
    DWORD reason,
    LPVOID)
{
    if(reason == DLL_PROCESS_ATTACH)
    {
        g_Module = hModule;

        DisableThreadLibraryCalls(
            hModule
        );


        HANDLE thread = CreateThread(
            nullptr,
            0,
            MainThread,
            hModule,
            0,
            nullptr
        );


        if(thread)
        {
            CloseHandle(thread);
        }
    }


    return TRUE;
}