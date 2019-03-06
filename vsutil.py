"""
VSUtil. A collection of general-purpose Vapoursynth functions to be reused in modules and scripts.
"""
from functools import reduce
import vapoursynth as vs
import re

core = vs.core


def get_subsampling(clip: vs.VideoNode) -> str:
    """
    Returns the subsampling of a clip in human-readable format.
    """
    if clip.format.subsampling_w == 1 and clip.format.subsampling_h == 1:
        css = '420'
    elif clip.format.subsampling_w == 1 and clip.format.subsampling_h == 0:
        css = '422'
    elif clip.format.subsampling_w == 0 and clip.format.subsampling_h == 0:
        css = '444'
    elif clip.format.subsampling_w == 2 and clip.format.subsampling_h == 2:
        css = '410'
    elif clip.format.subsampling_w == 2 and clip.format.subsampling_h == 0:
        css = '411'
    elif clip.format.subsampling_w == 0 and clip.format.subsampling_h == 1:
        css = '440'
    else:
        raise ValueError('Unknown subsampling')
    return css


def get_depth(clip: vs.VideoNode) -> int:
    """
    Returns the bitdepth of a clip as an integer.
    """
    return clip.format.bits_per_sample


def iterate(base, function, count):
    """
    Utility function that executes a given function for a given number of times.
    """
    return reduce(lambda v,_: function(v), range(count), base)


def insert_clip(clip: vs.VideoNode, insert: vs.VideoNode, start_frame: int) -> vs.VideoNode:
    """
    Convenience method to insert a shorter clip into a longer one.
    The inserted clip cannot go beyond the last frame of the source clip or an exception is raised.
    """
    if start_frame == 0:
        return insert + clip[insert.num_frames:]
    pre = clip[:start_frame]
    frame_after_insert = start_frame + insert.num_frames
    if frame_after_insert > clip.num_frames:
        raise ValueError('Inserted clip is too long')
    if frame_after_insert == clip.num_frames:
        return pre + insert
    post = clip[start_frame + insert.num_frames:]
    return pre + insert + post


def fallback(value, fallback_value):
    """
    Utility function that returns a value or a fallback if the value is None.
    """
    return fallback_value if value is None else value


def get_y(clip: vs.VideoNode) -> vs.VideoNode:
    """
    Helper to get the luma of a VideoNode.
    """
    return core.std.ShufflePlanes(clip, 0, vs.GRAY)


def split(clip: vs.VideoNode) -> list:
    """
    Returns a list of planes for the given input clip.
    """
    return [core.std.ShufflePlanes(clip, x, colorfamily=vs.GRAY) for x in range(clip.format.num_planes)]


def join(planes: list, family=vs.YUV) -> vs.VideoNode:
    """
    Joins the supplied list of planes into a YUV video node.
    """
    return core.std.ShufflePlanes(clips=planes, planes=[0], colorfamily=family)


def getw(h, ar=16 / 9, only_even=True):
    """
    returns width for image (taken from kagefunc)
    """
    w = h * ar
    w = int(round(w))
    if only_even:
        w = w // 2 * 2
    return w


def is_image(filename: str) -> bool:
    """
    Returns true if a filename refers to an image.
    """
    return mimetypes.types_map[os.path.splitext(filename)[-1]].startswith("image/")


def source(file: str, force_lsmas=False) -> vs.VideoNode:
    """
    Quick general import wrapper that automatically matches various sources with an appropriate indexing filter.
    """
    if file.startswith("file:///"):
        file = file[8::]

    if force_lsmas:
        return core.lsmas.LWLibavSource(file)
        
    if file.endswith(".d2v"):
        clip = core.d2v.Source(file)
    elif is_image(file):
        clip = core.imwri.Read(file)
    elif file.endswith(".m2ts"):
        clip = core.lsmas.LWLibavSource(file)
    else:
        clip = core.ffms2.Source(file)

    return clip 
        clip = core.lsmas.LWLibavSource(file)
    else:
        if file.endswith(".d2v"):
            clip = core.d2v.Source(file)
        elif is_image(file):
            clip = core.imwri.Read(file)
        else:
            if file.endswith(".m2ts"):
                clip = core.lsmas.LWLibavSource(file)
            else:
                clip = core.ffms2.Source(file)

    return clip
