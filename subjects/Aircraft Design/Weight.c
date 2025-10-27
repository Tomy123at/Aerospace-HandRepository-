#include <stdio.h>

#define N_TYPES   12
#define N_PHASES   6

int main() {
    const char *typeNames[N_TYPES] = {
        "1. Homebuilt",
        "2. Single Engine",
        "3. Twin Engine",
        "4. Agricultural",
        "5. Business Jets",
        "6. Regional TBP's",
        "7. Transport Jets",
        "8. Military Trainers",
        "9. Fighters",
        "10. Mil. Patrol/Bomb, Transport",
        "11. Flying Boats/Amphibious/Float",
        "12. Supersonic Cruise"
    };

    const char *phaseNames[N_PHASES] = {
        "Engine Start/Warm-up (1)",
        "Taxi              (2)",
        "Take-off          (3)",
        "Climb             (4)",
        "Descent           (7)",
        "Landing Taxi/Shut (8)"
    };

    /* tabla[type][phase] */
    double table[N_TYPES][N_PHASES] = {
        /* 1. Homebuilt */               {0.998, 0.998, 0.998, 0.995, 0.995, 0.995},
        /* 2. Single Engine */           {0.995, 0.997, 0.998, 0.992, 0.993, 0.993},
        /* 3. Twin Engine */             {0.992, 0.996, 0.996, 0.990, 0.992, 0.992},
        /* 4. Agricultural */            {0.996, 0.995, 0.998, 0.998, 0.992, 0.992},
        /* 5. Business Jets */           {0.990, 0.995, 0.995, 0.980, 0.990, 0.992},
        /* 6. Regional TBP's */          {0.990, 0.995, 0.995, 0.985, 0.985, 0.992},
        /* 7. Transport Jets */          {0.990, 0.990, 0.995, 0.980, 0.990, 0.992},
        /* 8. Military Trainers */       {0.990, 0.990, 0.990, 0.980, 0.990, 0.995},
        /* 9. Fighters */                {0.990, 0.990, 0.990,   0.96, 0.990, 0.995},
        /*10. Mil. Patrol/Bomb, Transport*/ {0.990,0.990, 0.995, 0.980, 0.990, 0.992},
        /*11. Flying Boats/Amphibious/Float*/ {0.992,0.990,0.996,0.985,0.990,0.990},
        /*12. Supersonic Cruise */       {0.990, 0.995, 0.995,   0.92, 0.985, 0.992}
    };

    int choice;
    printf("Seleccione tipo de aeronave:\n");
    for (int i = 0; i < N_TYPES; i++) {
        printf("  %s\n", typeNames[i]);
    }
    printf("Ingrese el número (1-%d): ", N_TYPES);
    if (scanf("%d", &choice) != 1 || choice < 1 || choice > N_TYPES) {
        printf("Opción inválida.\n");
        return 1;
    }

    int idx = choice - 1;
    printf("\nFuel‑Fractions para %s:\n", typeNames[idx]);
    for (int p = 0; p < N_PHASES; p++) {
        printf("  %s: %.3f\n", phaseNames[p], table[idx][p]);
    }

    return 0;
}
