#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
import math
import sys
import os
from PIL import Image
from io import BytesIO
from chara_wan.model import WanFile, SequenceFrame, MetaFramePiece, FrameOffset, ImgPiece, \
    MINUS_FRAME, DIM_TABLE, TEX_SIZE, DEBUG_PRINT








def ExportWan(wan):
    out_file = BytesIO()

    out_file.write(b'\x53\x49\x52\x30')
    sir0_ptrs = [4, 8]
    # 4- WAN header ptr
    write_ptr(out_file, 0, sir0_ptrs)
    # 8 - SIR0 pointer list ptr
    write_ptr(out_file, 0, sir0_ptrs)
    # 12 - zeroes
    out_file.write((0).to_bytes(4, 'little'))
    # Metaframes
    ptrMetaFrames = []
    for metaFrame in wan.frameData:
        ptrMetaFrames.append(out_file.tell())
        for piece in metaFrame:
            out_file.write(piece.imgIndex.to_bytes(2, 'little', signed=True))
            out_file.write((0).to_bytes(2, 'little'))
            out_file.write((piece.attr0).to_bytes(2, 'little'))
            out_file.write((piece.attr1).to_bytes(2, 'little'))
            out_file.write((piece.attr2).to_bytes(2, 'little'))

    # animation sequences
    animSeqPtrList = []
    for anim_group in wan.animGroupData:
        groupSequencesPtrs = []
        for sequence in anim_group:
            groupSequencesPtrs.append(out_file.tell())
            for animFrame in sequence:
                out_file.write(animFrame.duration.to_bytes(1, 'little'))
                out_file.write(animFrame.flag.to_bytes(1, 'little'))
                out_file.write(animFrame.frameIndex.to_bytes(2, 'little'))
                out_file.write(animFrame.offset[0].to_bytes(2, 'little', signed=True))
                out_file.write(animFrame.offset[1].to_bytes(2, 'little', signed=True))
                out_file.write(animFrame.shadow[0].to_bytes(2, 'little', signed=True))
                out_file.write(animFrame.shadow[1].to_bytes(2, 'little', signed=True))
            # write a null
            out_file.write((0).to_bytes(12, 'little'))
        if len(anim_group) > 0:
            while len(groupSequencesPtrs) < 8:
                groupSequencesPtrs.append(groupSequencesPtrs[-1])
        animSeqPtrList.append(groupSequencesPtrs)

    padUntilDiv(out_file, b'\xAA', 4)

    # img data
    ptrImgs = []
    for img in wan.imgData:
        zSort = img.zSort
        imgTable = []
        # write pixel data
        for pxStrip in img.imgPx:
            hasNonZero = False
            for px in pxStrip:
                if px > 0:
                    hasNonZero = True
                    break
            if hasNonZero:
                imgTable.append((out_file.tell(), len(pxStrip)))
                for px in pxStrip:
                    out_file.write(px.to_bytes(1, 'little'))
            else:
                imgTable.append((0, len(pxStrip)))

        ptrImgs.append(out_file.tell())
        for img_write in imgTable:
            # pixelSource
            write_ptr(out_file, img_write[0], sir0_ptrs)
            # amt
            out_file.write(img_write[1].to_bytes(2, 'little'))
            # unk#14
            out_file.write((0).to_bytes(2, 'little'))
            # unk#2
            out_file.write(zSort.to_bytes(4, 'little'))
        out_file.write((0).to_bytes(12, 'little'))

    # palette data
    ptrPaletteDataBlock = out_file.tell()
    nbColorsPerRow = 0
    for palette_row in wan.customPalette:
        if len(palette_row) > 1:
            nbColorsPerRow = len(palette_row)
        for palette in palette_row:
            # R
            out_file.write(palette[0].to_bytes(1, 'little'))
            # G
            out_file.write(palette[1].to_bytes(1, 'little'))
            # B
            out_file.write(palette[2].to_bytes(1, 'little'))
            # X
            out_file.write(b'\x80')
    # palette info
    ptrPaletteInfo = out_file.tell()
    write_ptr(out_file, ptrPaletteDataBlock, sir0_ptrs)
    # Unk#3
    out_file.write((0).to_bytes(2, 'little'))
    # colors per row
    out_file.write(nbColorsPerRow.to_bytes(2, 'little'))
    # Unk#4
    out_file.write((0).to_bytes(2, 'little'))
    # Unk#5
    out_file.write((255).to_bytes(2, 'little'))
    # 4 bytes of zeroes indicating end of palette info?
    out_file.write((0).to_bytes(4, 'little'))

    # Metaframes ref table
    ptrMetaFramesRefTable = out_file.tell()
    for metaframe_ptr in ptrMetaFrames:
        write_ptr(out_file, metaframe_ptr, sir0_ptrs)

    # Particle offsets table
    ptrOffsetsTable = out_file.tell()
    for offset in wan.offsetData:
        out_file.write(offset.head[0].to_bytes(2, 'little', signed=True))
        out_file.write(offset.head[1].to_bytes(2, 'little', signed=True))
        out_file.write(offset.lhand[0].to_bytes(2, 'little', signed=True))
        out_file.write(offset.lhand[1].to_bytes(2, 'little', signed=True))
        out_file.write(offset.rhand[0].to_bytes(2, 'little', signed=True))
        out_file.write(offset.rhand[1].to_bytes(2, 'little', signed=True))
        out_file.write(offset.center[0].to_bytes(2, 'little', signed=True))
        out_file.write(offset.center[1].to_bytes(2, 'little', signed=True))

    # AnimSequenceTable
    animGroupSequencePtrs = []
    for groupSequencesPtrs in animSeqPtrList:
        animGroupSequencePtrs.append(out_file.tell())
        for animSeqPtr in groupSequencesPtrs:
            write_ptr(out_file, animSeqPtr, sir0_ptrs)
        if len(groupSequencesPtrs) == 0:
            out_file.write((0).to_bytes(4, 'little'))

    # AnimGroupTable
    ptrAnimGroupTable = out_file.tell()
    for idx, groupSequencesPtrs in enumerate(animSeqPtrList):
        groupPtr = animGroupSequencePtrs[idx]
        if len(groupSequencesPtrs) == 0:
            groupPtr = 0
        # location of the first sequence in the group
        write_ptr(out_file, groupPtr, sir0_ptrs)
        # number of sequences in group
        out_file.write(len(groupSequencesPtrs).to_bytes(2, 'little'))
        # Unk#16
        out_file.write((0).to_bytes(2, 'little'))

    # Image Data Table
    ptrImageDataTable = out_file.tell()
    for img_ptr in ptrImgs:
        write_ptr(out_file, img_ptr, sir0_ptrs)

    # compute max block space
    max_blocks = 0
    for idx, metaFrame in enumerate(wan.frameData):
        cur_tile = 0
        for piece in metaFrame:
            if piece.imgIndex != MINUS_FRAME:
                twidth, theight = DIM_TABLE[piece.getResolutionType()]
                blocks_occupied = max(1, twidth * theight // 4)
                cur_tile += blocks_occupied
        max_blocks = max(max_blocks, cur_tile)

    # AnimInfo
    ptrAnimInfo = out_file.tell()
    write_ptr(out_file, ptrMetaFramesRefTable, sir0_ptrs)
    write_ptr(out_file, ptrOffsetsTable, sir0_ptrs)
    write_ptr(out_file, ptrAnimGroupTable, sir0_ptrs)
    out_file.write(len(animSeqPtrList).to_bytes(2, 'little'))
    # Unk#6
    out_file.write(max_blocks.to_bytes(2, 'little'))
    # Unk#7
    out_file.write((0).to_bytes(2, 'little'))
    # Unk#8
    out_file.write((0).to_bytes(2, 'little'))
    # Unk#9
    out_file.write((0).to_bytes(2, 'little'))
    # Unk#10
    out_file.write((0).to_bytes(2, 'little'))

    # Image Data Info
    ptrImageDataInfo = out_file.tell()
    write_ptr(out_file, ptrImageDataTable, sir0_ptrs)
    write_ptr(out_file, ptrPaletteInfo, sir0_ptrs)
    # Unk#13
    out_file.write((0).to_bytes(2, 'little'))
    # Is256ColorSpr - never
    out_file.write((0).to_bytes(2, 'little'))
    # Unk#11
    if len(ptrImgs) > 0:
        out_file.write((1).to_bytes(2, 'little'))
    else:
        out_file.write((0).to_bytes(2, 'little'))
    # nbImgs
    out_file.write(len(ptrImgs).to_bytes(2, 'little'))

    # WAN header
    ptrWAN = out_file.tell()
    write_ptr(out_file, ptrAnimInfo, sir0_ptrs)
    write_ptr(out_file, ptrImageDataInfo, sir0_ptrs)
    # img type - always 1 for character sprites
    out_file.write((1).to_bytes(2, 'little'))
    # Unk#12
    out_file.write((0).to_bytes(2, 'little'))

    # fill with AA until divisible by 16
    padUntilDiv(out_file, b'\xAA', 16)

    # sir0 pointers
    ptrSir0 = out_file.tell()
    for idx, offset in enumerate(sir0_ptrs):
        offset_to_encode = offset
        if idx > 0:
            offset_to_encode -= sir0_ptrs[idx - 1]
        # This tells the loop whether it needs to encode null bytes, if at least one higher byte was non-zero
        has_higher_non_zero = False
        # Encode every bytes of the 4 bytes integer we have to
        for i in range(4, 0, -1):
            currentbyte = (offset_to_encode >> (7 * (i - 1))) & 0x7F
            # the lowest byte to encode is special
            if i == 1:
                # If its the last byte to append, leave the highest bit to 0 !
                out_file.write(currentbyte.to_bytes(1, 'little'))
            elif currentbyte != 0 or has_higher_non_zero:
                # if any bytes but the lowest one! If not null OR if we have encoded a higher non-null byte before!
                out_file.write((currentbyte | 0x80).to_bytes(1, 'little'))
                has_higher_non_zero = True
    # null terminate the sir0 header list
    out_file.write(b'\x00')

    # fill with AA until divisible by 16
    padUntilDiv(out_file, b'\xAA', 16)

    out_file.seek(4)
    out_file.write(ptrWAN.to_bytes(4, 'little'))
    out_file.write(ptrSir0.to_bytes(4, 'little'))

    out_file.seek(0)
    return out_file.read()







def padUntilDiv(out_file, bt, div):
    fill = div - out_file.tell() % div
    if fill != div:
        for ii in range(fill):
            out_file.write(bt)


def write_ptr(out_file, value, sir0_ptrs):
    if value > 0:
        sir0_ptrs.append(out_file.tell())
    out_file.write(value.to_bytes(4, 'little'))





