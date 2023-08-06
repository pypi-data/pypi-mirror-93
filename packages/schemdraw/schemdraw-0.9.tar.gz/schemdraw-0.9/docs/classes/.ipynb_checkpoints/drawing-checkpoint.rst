
Drawing
=======

.. autoclass:: schemdraw.Drawing
    :members:
    :exclude-members: labelI, labelI_inline, loopI

Element
=======


.. autoclass:: schemdraw.elements.Element
    :members:
    :exclude-members: add_label


Element2Term
============

.. autoclass:: schemdraw.elements.Element2Term
    :members:


ElementDrawing
==============

.. autoclass:: schemdraw.elements.ElementDrawing
    :members:


Element Style
=============

.. py:function:: schemdraw.elements.style(style)

    Set global element style

    :param style: dictionary of {elementname: Element} to change the element module namespace. Use `elements.STYLE_US` or `elements.STYLE_IEC` to define U.S. or European/IEC element styles.

