r"""
Curves over number fields
=========================

Let `K` be a number field and `Y` a smooth projective curve over `K`. We would
like to be able to compute certain arithmetic invariants attached to `Y`, e.g.

- the *`L`-function* `L(Y,s)` of `Y`
- the *conductor* `N_Y` of `Y`
- etc.


Then `Y` has *good reduction* at all but finitely many prime ideals `\mathfrak{p}`
of `K` (and *bad reduction* at the remaining ones).

In this module we realize a class ``CurvesOverNumberFields`` with some
functionality for computing the invariants mentioned above. Of course, the hard
work is relegated to the modules in ``mclf.semistable_reduction``.

``CurvesOverNumberFields`` is a subclass of ``SmoothProjectiveCurve`` and is
instantiated by its parent class if the  constant base field of the created
curve is a number field.

AUTHORS:

- Stefan Wewers (2018-8-1): initial version


EXAMPLES::

    sage: from mclf import *


.. TODO::


"""

#*****************************************************************************
#       Copyright (C) 2016-2018 Stefan Wewers <stefan.wewers@uni-ulm.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
#*****************************************************************************

from sage.all import NumberField, NumberFields, QQ
from mclf.curves.smooth_projective_curves import SmoothProjectiveCurve



class CurveOverNumberField(SmoothProjectiveCurve):
    r""" Return a curve over a number field

    This class is not called directly, so there is no function ``__init__``.

    """

    def semistable_model(self, p):
        r""" Return the semistable model of this curves at a prime

        INPUT:

        - ``p`` -- a prime ideal of the constant base field, or a prime number
                   if the the constant base field is `\mathbb{Q}`

        OUTPUT: the object of the class ``SemistabeModels`` representing
        a semistable model of the curve at ``p``.

        NOTE: at the moment, this works only over `\mathbb{Q}`

        """
        from mclf.semistable_reduction.semistable_models import SemistableModel
        K = self.constant_base_field()
        if not K is QQ:
            raise NotImplementedError('Semistable reduction is only implemented over Q')
        if hasattr(self, "_semistable_models"):
            ss_models = self._semistable_models
        else:
            ss_models = {}
        if p in ss_models.keys():
            return ss_models[p]
        else:
            vp = QQ.valuation(p)
            ss_models[p] = SemistableModel(self, vp)
            self._semistable_models = ss_models
            return ss_models[p]


    def reduction_type(self, p):
        r""" Return the type of the semistable reduction of this curve at p.

        INPUT:

        - ``p`` -- a prime ideal of the constant base field of this curve.

        OUTPUT: the 'type' of the special fiber of the semistable reduction
        of this curve at `p`.

        For the moment, this is only implemented for some special classes of
        curves.

        """
        raise NotImplementedError("Reduction type for general curves is not defined.")


    def conductor_exponent(self, p):
        r""" Return the conductor exponent of this curve at p.

        INPUT:

        - ``p`` -- a prime ideal of the constant base field of this curve.

        OUTPUT: the exponent of `p` in the conductor of this curve.

        """
        return self.semistable_model(p).conductor_exponent()
