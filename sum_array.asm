;
; initialized data is put in the .data segment
;
segment .data


;
; uninitialized data is put in the .bss segment
;
segment .bss

;
; code is put in the .text segment
;
segment .text

        global  _sum_array
_sum_array: 
        ; void _sum_array(float* input, int size, int* output);
        ; [ebp + 8] = int* input
        ; [ebp + 12] = int size
        ; [ebp + 16] = int* output
        push ebp
        mov ebp, esp

        mov eax, [ebp+8]        ; eax = float* input
        mov ecx, [ebp+16]       ; ecx = int* output
        mov edx, 0              ; edx = i

for_loop:
        cmp edx, [ebp+12]       ; comparar i con size
        jge end_loop            ; jump if (edx) greater or equal
        
        add dword [eax+edx*4], edx ; input[i] += 1

        fld dword [eax+edx*4]   ; guardar float en la pila de la FPU
        fistp dword [ecx+edx*4] ; pasamos a entero y guardamos en output[i]
        inc dword [ecx+edx*4]   ; output[i] += 1

        inc edx ; i++
        jmp for_loop

end_loop:

        mov esp, ebp
        pop ebp
        ret

