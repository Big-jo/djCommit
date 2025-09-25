#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <termios.h>

#ifdef __APPLE__
#include <AudioToolbox/AudioToolbox.h>
#endif

#ifdef __linux__
#include <sys/ioctl.h>
#include <linux/kd.h>
#endif

// Function to play a beep with specific frequency and duration
void play_beep(int frequency, int duration_ms) {
#ifdef __APPLE__
    // macOS: Use AudioToolbox for better sound
    AudioServicesPlaySystemSound(kSystemSoundID_UserPreferredAlert);
#elif __linux__
    // Linux: Try console beep
    if (ioctl(STDOUT_FILENO, KDMKTONE, (frequency << 16) | (1193180 / frequency)) == 0) {
        usleep(duration_ms * 1000);
        ioctl(STDOUT_FILENO, KDMKTONE, 0); // Stop beep
    } else {
        // Fallback to terminal bell
        printf("\a");
        fflush(stdout);
    }
#else
    // Windows or other: Use terminal bell
    printf("\a");
    fflush(stdout);
#endif
}

// Function to play a sequence of beeps
void play_sequence(int frequencies[], int durations[], int count) {
    for (int i = 0; i < count; i++) {
        if (frequencies[i] == 0) {
            // Rest - just sleep for the duration
            usleep(durations[i] * 1000);
        } else {
            play_beep(frequencies[i], durations[i]);
        }
        if (i < count - 1) {
            usleep(50000); // 50ms pause between notes
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <sound_type>\n", argv[0]);
        printf("Sound types: clown, mario, desperado, test\n");
        return 1;
    }
    
    char *sound_type = argv[1];
    
    if (strcmp(sound_type, "clown") == 0) {
        // Circus/clown theme - "Entry of the Gladiators" opening
        int freqs[] = {
            523, 523, 523, 523, 523, 523, 523, 523,  // C5 repeated
            659, 659, 659, 659, 659, 659, 659, 659,  // E5 repeated
            523, 523, 523, 523, 523, 523, 523, 523,  // C5 repeated
            440, 440, 440, 440, 440, 440, 440, 440,  // A4 repeated
            523, 659, 784, 880, 784, 659, 523, 440   // C-E-G-A-G-E-C-A
        };
        int durations[] = {
            200, 200, 200, 200, 200, 200, 200, 200,
            200, 200, 200, 200, 200, 200, 200, 200,
            200, 200, 200, 200, 200, 200, 200, 200,
            200, 200, 200, 200, 200, 200, 200, 200,
            300, 300, 300, 400, 300, 300, 300, 400
        };
        play_sequence(freqs, durations, 40);
        
    } else if (strcmp(sound_type, "mario") == 0) {
        // Super Mario Bros. main theme - the iconic opening
        int freqs[] = {
            659, 659, 0, 659, 0, 523, 659, 0, 784, 0, 0, 0, 392, 0, 0, 0,  // Opening phrase
            523, 0, 392, 0, 330, 0, 440, 0, 494, 0, 466, 440, 0, 392, 659, 784,  // Second phrase
            880, 0, 659, 523, 440, 0, 392, 0, 330, 0, 440, 0, 494, 0, 466, 440,  // Third phrase
            392, 0, 659, 523, 440, 0, 392, 0, 330, 0, 440, 0, 494, 0, 466, 440   // Final phrase
        };
        int durations[] = {
            200, 200, 100, 200, 100, 200, 200, 100, 200, 100, 100, 100, 200, 100, 100, 100,
            200, 100, 200, 100, 200, 100, 200, 100, 200, 100, 200, 200, 100, 200, 200, 200,
            200, 100, 200, 200, 200, 100, 200, 100, 200, 100, 200, 100, 200, 100, 200, 200,
            200, 100, 200, 200, 200, 100, 200, 100, 200, 100, 200, 100, 200, 100, 200, 200
        };
        play_sequence(freqs, durations, 64);
        
    } else if (strcmp(sound_type, "desperado") == 0) {
        // Eagles "Desperado" - the iconic opening melody
        int freqs[] = {
            523, 0, 659, 0, 784, 0, 659, 0, 523, 0, 440, 0, 392, 0, 440, 0,  // "Desperado, why don't you come to your senses"
            523, 0, 659, 0, 784, 0, 880, 0, 784, 0, 659, 0, 523, 0, 440, 0,  // "You've been out ridin' fences for so long now"
            392, 0, 440, 0, 523, 0, 659, 0, 523, 0, 440, 0, 392, 0, 330, 0,  // "Oh, you're a hard one"
            440, 0, 523, 0, 659, 0, 784, 0, 659, 0, 523, 0, 440, 0, 392, 0   // "But I know that you have your reasons"
        };
        int durations[] = {
            400, 100, 400, 100, 400, 100, 400, 100, 400, 100, 400, 100, 400, 100, 400, 100,
            400, 100, 400, 100, 400, 100, 400, 100, 400, 100, 400, 100, 400, 100, 400, 100,
            400, 100, 400, 100, 400, 100, 400, 100, 400, 100, 400, 100, 400, 100, 400, 100,
            400, 100, 400, 100, 400, 100, 400, 100, 400, 100, 400, 100, 400, 100, 400, 100
        };
        play_sequence(freqs, durations, 64);
        
    } else if (strcmp(sound_type, "test") == 0) {
        // Test sound: simple beep
        play_beep(800, 300);
        
    } else {
        printf("Unknown sound type: %s\n", sound_type);
        return 1;
    }
    
    return 0;
}
