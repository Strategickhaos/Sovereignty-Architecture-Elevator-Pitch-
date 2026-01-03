" FlameTranscribe_SAGCO CTF Vim Macros
" Strategickhaos DAO LLC | INV-093
" 
" SAGCO Face Mappings for Rubik's Cube CTF Methodology
" 
" Usage:
"   @s - S-Face: Transcribe (DNA)
"   @a - A-Face: Analyze (Hex)
"   @g - G-Face: Generate (Binary)
"   @c - C-Face: Certify (MRVE Seal)
"   @o - O-Face: Output (NFT)
"   @r - Full pipeline (all faces)
"   <leader>tr - Execute full pipeline
"   <leader>? - Show SAGCO reference

" ============================================================================
" SAGCO Face Macros
" ============================================================================

" S-Face: Source/Transcribe - DNA transcription
let @s = ':!python3 flame_transcribe.py % --face S
'

" A-Face: Analyze - Hexadecimal analysis
let @a = ':%!xxd
'

" G-Face: Generate - Binary generation
let @g = ':!python3 -c "import sys; content=sys.stdin.read(); print('' ''.join(bin(ord(c))[2:].zfill(8) for c in content))" < %
'

" C-Face: Certify/Seal - MRVE cryptographic seal
let @c = ':!python3 flame_transcribe.py % --face C
'

" O-Face: Output - NFT generation
let @o = ':!python3 flame_transcribe.py % --face O
'

" Full CTF sequence - Execute all faces in order
let @r = ':normal @s@a@g@c@o
'

" ============================================================================
" Leader Key Mappings
" ============================================================================

" Execute full pipeline
nnoremap <leader>tr :!python3 flame_transcribe.py %<CR>

" Execute individual faces
nnoremap <leader>ts :!python3 flame_transcribe.py % --face S<CR>
nnoremap <leader>ta :!python3 flame_transcribe.py % --face A<CR>
nnoremap <leader>tg :!python3 flame_transcribe.py % --face G<CR>
nnoremap <leader>tc :!python3 flame_transcribe.py % --face C<CR>
nnoremap <leader>to :!python3 flame_transcribe.py % --face O<CR>

" Show SAGCO reference
nnoremap <leader>? :!python3 flame_transcribe.py --sagco<CR>

" Quick DNA transcribe for current word
nnoremap <leader>tw viw:!python3 flame_transcribe.py --face S --quiet<CR>

" ============================================================================
" CTF Methodology Commands
" ============================================================================

" Reconnaissance phase (S-Face)
command! CTFRecon !python3 flame_transcribe.py % --face S

" Enumeration phase (A-Face)
command! CTFEnum %!xxd

" Exploitation phase (G-Face)
command! CTFExploit !python3 flame_transcribe.py % --face G

" Persistence phase (C-Face)
command! CTFPersist !python3 flame_transcribe.py % --face C

" Exfiltration phase (O-Face)
command! CTFExfil !python3 flame_transcribe.py % --face O

" Full CTF workflow
command! CTFFull !python3 flame_transcribe.py %

" ============================================================================
" Visual Mode Mappings
" ============================================================================

" Transcribe visual selection
vnoremap <leader>ts :!python3 flame_transcribe.py --face S --quiet<CR>

" Hex dump visual selection
vnoremap <leader>ta :!xxd<CR>

" Binary encode visual selection
vnoremap <leader>tg :!python3 -c "import sys; content=sys.stdin.read(); print(' '.join(bin(ord(c))[2:].zfill(8) for c in content))"<CR>

" ============================================================================
" Helper Functions
" ============================================================================

" Function to transcribe current buffer and open in split
function! FlameTranscribeSplit()
    " Save current buffer
    write
    
    " Create new vertical split
    vnew
    
    " Run pipeline and capture output
    execute 'read !python3 flame_transcribe.py ' . expand('#')
    
    " Set buffer options
    setlocal buftype=nofile
    setlocal bufhidden=hide
    setlocal noswapfile
    
    " Go to top
    normal! gg
endfunction

" Command for split transcription
command! TSplit call FlameTranscribeSplit()
nnoremap <leader>tsp :TSplit<CR>

" Function to show SAGCO reference in split
function! SAGCOReference()
    " Create new split
    split
    
    " Create new buffer
    enew
    
    " Insert SAGCO reference
    execute 'read !python3 flame_transcribe.py --sagco'
    
    " Set buffer options
    setlocal buftype=nofile
    setlocal bufhidden=hide
    setlocal noswapfile
    setlocal readonly
    
    " Go to top
    normal! gg
    
    " Resize
    resize 15
endfunction

" Command for SAGCO reference
command! SAGCORef call SAGCOReference()
nnoremap <leader>ref :SAGCORef<CR>

" ============================================================================
" Rubik's Cube CTF Visual Guide
" ============================================================================

" Function to display Rubik CTF mapping
function! RubikCTFGuide()
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║  RUBIK CTF FACE MAPPING - FlameTranscribe_SAGCO          ║"
    echo "╠═══════════════════════════════════════════════════════════╣"
    echo "║         ┌─────────┐                                       ║"
    echo "║         │    A    │  (Hex/Analyze)                       ║"
    echo "║         │ 41h GCT │                                       ║"
    echo "║ ┌───────┼─────────┼───────┬─────────┐                   ║"
    echo "║ │   S   │    G    │   C   │    O    │                   ║"
    echo "║ │ 53h   │   47h   │  43h  │   4Fh   │                   ║"
    echo "║ │ AGC   │   GGA   │  TGC  │   TAA   │                   ║"
    echo "║ │Source │Generate │Certify│ Output  │                   ║"
    echo "║ └───────┼─────────┼───────┴─────────┘                   ║"
    echo "║         │ (Back)  │                                       ║"
    echo "║         │  ???    │                                       ║"
    echo "║         └─────────┘                                       ║"
    echo "╠═══════════════════════════════════════════════════════════╣"
    echo "║ CTF Phase   │ Rubik Phase │ Face │ Commands              ║"
    echo "╟─────────────┼─────────────┼──────┼───────────────────────╢"
    echo "║ Recon       │ White Cross │  S   │ @s, <leader>ts        ║"
    echo "║ Enum        │ F2L         │  A   │ @a, <leader>ta        ║"
    echo "║ Exploit     │ OLL         │  G   │ @g, <leader>tg        ║"
    echo "║ Persist     │ PLL         │  C   │ @c, <leader>tc        ║"
    echo "║ Exfil       │ Solve       │  O   │ @o, <leader>to        ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
endfunction

command! RubikGuide call RubikCTFGuide()
nnoremap <leader>rg :RubikGuide<CR>

" ============================================================================
" Auto-commands
" ============================================================================

" Highlight SAGCO characters
augroup SAGCOHighlight
    autocmd!
    autocmd BufEnter * syntax match SAGCOChar /[SAGCO]/
    autocmd BufEnter * highlight SAGCOChar ctermfg=cyan guifg=#00ffff
augroup END

" ============================================================================
" Status Line Integration
" ============================================================================

" Add SAGCO indicator to status line
function! SAGCOStatus()
    let l:char = getline('.')[col('.')-1]
    if l:char =~ '[SAGCO]'
        return ' [SAGCO:' . l:char . '] '
    endif
    return ''
endfunction

" Optional: Add to statusline
" set statusline+=%{SAGCOStatus()}

" ============================================================================
" Documentation
" ============================================================================

" Show this documentation
function! ShowSAGCODocs()
    echo "FlameTranscribe_SAGCO Vim Macros - INV-093"
    echo ""
    echo "Macros:"
    echo "  @s - DNA Transcription"
    echo "  @a - Hex Analysis"
    echo "  @g - Binary Generation"
    echo "  @c - MRVE Seal"
    echo "  @o - NFT Output"
    echo "  @r - Full Pipeline"
    echo ""
    echo "Leader mappings (<leader> = backslash by default):"
    echo "  <leader>tr  - Full pipeline"
    echo "  <leader>ts  - S-Face only"
    echo "  <leader>ta  - A-Face only"
    echo "  <leader>tg  - G-Face only"
    echo "  <leader>tc  - C-Face only"
    echo "  <leader>to  - O-Face only"
    echo "  <leader>?   - SAGCO reference"
    echo "  <leader>ref - SAGCO reference in split"
    echo "  <leader>rg  - Rubik CTF guide"
    echo ""
    echo "Commands:"
    echo "  :CTFFull    - Execute full pipeline"
    echo "  :CTFRecon   - Reconnaissance (S-Face)"
    echo "  :CTFEnum    - Enumeration (A-Face)"
    echo "  :CTFExploit - Exploitation (G-Face)"
    echo "  :CTFPersist - Persistence (C-Face)"
    echo "  :CTFExfil   - Exfiltration (O-Face)"
    echo "  :TSplit     - Transcribe in split window"
    echo "  :RubikGuide - Show Rubik CTF mapping"
endfunction

command! SAGCOHelp call ShowSAGCODocs()
nnoremap <leader>help :SAGCOHelp<CR>

" ============================================================================
" Installation Message
" ============================================================================

" Display on first load
if !exists('g:sagco_loaded')
    let g:sagco_loaded = 1
    echo "FlameTranscribe_SAGCO Vim macros loaded! Type :SAGCOHelp for usage."
endif
