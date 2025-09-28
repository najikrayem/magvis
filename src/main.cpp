#include <glad/gl.h>
#include <SDL3/SDL.h>
#include <SDL3/SDL_main.h>
#include <spdlog/spdlog.h>
#include <iostream>

#define OPENGL_REQUEST_MAJOR 3
#define OPENGL_REQUEST_MINOR 3
#define OPENGL_REQUEST_PROFILE SDL_GL_CONTEXT_PROFILE_CORE

// return true if successful, false for critical (exit)
bool mgvz_init_sdl(){
    if (!SDL_Init(SDL_INIT_VIDEO)) {
        SPDLOG_CRITICAL("Error initializing SDL3: {}. EXITING.", SDL_GetError());
        return false;
    }
    SPDLOG_INFO("SDL3 initialized.");
    return true;
}


// return 0 on success, 1 on critical fail, and 2 on warn (e.g. if requested attributes not granted)
int mgvz_create_window(SDL_Window** window){
    bool warn = false;

    // request window attributes
    SPDLOG_INFO("Set OpenGL major attribute: {}", OPENGL_REQUEST_MAJOR);
    if (!SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, OPENGL_REQUEST_MAJOR)){
        SPDLOG_WARN("Could not set OpenGL major attr: {}", SDL_GetError());
        warn = true;
    }
    SPDLOG_INFO("Set OpenGL minor attribute: {}", OPENGL_REQUEST_MINOR);
    if (!SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, OPENGL_REQUEST_MINOR)){
        SPDLOG_WARN("Could not set OpenGL minor attr: {}", SDL_GetError());
        warn = true;
    }
    SPDLOG_INFO("Set OpenGL profile attribute: {}", OPENGL_REQUEST_PROFILE);
    if (!SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, OPENGL_REQUEST_PROFILE)){
        SPDLOG_WARN("Could not set OpenGL profile attr: {}", SDL_GetError());
        warn = true;
    }

    // create window
    *window = SDL_CreateWindow(
        "MagViz",      // window title
        800,                         // width
        800,                         // height
        SDL_WINDOW_RESIZABLE         // flags (visible)
        | SDL_WINDOW_OPENGL
    );
    if (!*window) {
        SPDLOG_CRITICAL("Failed to create window: {}. EXITING.", SDL_GetError());
        SDL_Quit();
        return 1;
    }
    SPDLOG_INFO("Window created.");


    //check if requested attributes were truly granted
    int major, minor, profile;
    if(!SDL_GL_GetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, &major)){
        SPDLOG_WARN("Could not get OpenGL major attr: {}", SDL_GetError());
        warn = true;
    }else{
        SPDLOG_INFO("Assigned OpenGL Major: {}", major);
        if (major != OPENGL_REQUEST_MAJOR){
            SPDLOG_WARN("Requested major attr val does not match assigned");
            warn = true;
        }
    }
    if(!SDL_GL_GetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, &minor)){
        SPDLOG_WARN("Could not get OpenGL minor attr: {}", SDL_GetError());
        warn = true;
    }else{
        SPDLOG_INFO("Assigned OpenGL minor: {}", minor);
        if (minor != OPENGL_REQUEST_MINOR){
            SPDLOG_WARN("Requested minor attr val does not match assigned");
            warn = true;
        }
    }
    if(!SDL_GL_GetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, &profile)){
        SPDLOG_WARN("Could not get OpenGL profile attr: {}", SDL_GetError());
        warn = true;
    }else{
        SPDLOG_INFO("Assigned OpenGL profil: {}", profile);
        if (profile != OPENGL_REQUEST_PROFILE){
            SPDLOG_WARN("Requested profile attr val does not match assigned");
            warn = true;
        }
    }

    if (warn){
        return 2;
    }
    return 0;
}


int main(int argc, char **argv) {

    SPDLOG_INFO("MagViz Starting...");
    
    // init
    if (!mgvz_init_sdl()){
        return 1;
    }


    //create window
    SDL_Window* window = nullptr;
    if (mgvz_create_window(&window) == 1){
        return 1;
    }


    //create opengl context
    SDL_GLContext glcontext = SDL_GL_CreateContext(window);
    if (!glcontext){
        SPDLOG_CRITICAL("Failed to create gl context: {}. EXITING.", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }
    SPDLOG_INFO("GL context created.");


    // make context current
    if (!SDL_GL_MakeCurrent(window, glcontext)){
        SPDLOG_CRITICAL("Failed to make context current: {}. EXITING.", SDL_GetError());
        SDL_GL_DestroyContext(glcontext);
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }
    

    //glad to get ptrs
    int gl_ver = gladLoadGL((GLADloadfunc) SDL_GL_GetProcAddress);
    if (gl_ver == 0){
        SPDLOG_CRITICAL("Failed to load GL function pointers: {}. EXITING.", SDL_GetError());
        SDL_GL_DestroyContext(glcontext);
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }
    SPDLOG_INFO("OpenGL version: {}", reinterpret_cast<const char*>(glGetString(GL_VERSION)));
    SPDLOG_INFO("Renderer: {}",  reinterpret_cast<const char*>(glGetString(GL_RENDERER)));



    // check if adaptive vsync is supported
    if (!SDL_GL_SetSwapInterval(-1)){
        SPDLOG_WARN("Adaptive VSYNC not supported");
    }


    // Main loop: wait for quit event
    bool running = true;
    SDL_Event event;

    float r=0,g=0,b=0,a=0;
    while (running) {
        // Poll for events (keyboard, mouse, window, etc.)
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_EVENT_QUIT) { // user clicked the close button
                running = false;
            }
        }

        r += 0.0001;
        //g += 0.0002;
        //b += 0.0003;

        if(r>1)
            r = 0;
        if(g>1)
            g = 0;
        if(b>1)
            r = 0;

        glClearColor(r,g,b,a);
        glClear(GL_COLOR_BUFFER_BIT);
        SDL_GL_SwapWindow(window);
    }

    // 4. Clean up
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}