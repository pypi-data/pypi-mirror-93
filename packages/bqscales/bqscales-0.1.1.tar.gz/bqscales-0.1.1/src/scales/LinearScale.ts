/* Copyright 2015 Bloomberg Finance L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import * as d3Scale from 'd3-scale';
import { LinearScaleModel } from './LinearScaleModel';

import {
  Scale
} from './Scale';


export
class LinearScale extends Scale {
  render() {
    super.render();
    if(this.model.domain.length > 0) {
      this.scale.domain(this.model.domain);
    }
  }

  protected createD3Scale() {
    this.scale = d3Scale.scaleLinear();
  }

  expandDomain(oldRange: any[], newRange: any[]) {
    // If you have a current range and then a new range and want to
    // expand the domain to expand to the new range but keep it
    // consistent with the previous one, this is the function you use.

    // The following code is required to make a copy of the actual
    // state of the scale. Referring to the model domain and then
    // setting the range to be the old range in case it is not.
    const unpaddedScale = this.scale.copy();

    // To handle the case for a clamped scale for which we have to
    // expand the domain, the copy should be unclamped.
    unpaddedScale.clamp(false);
    unpaddedScale.domain(this.model.domain);
    unpaddedScale.range(oldRange);
    this.scale.domain(newRange.map((limit) => {
      return unpaddedScale.invert(limit);
    }));
  }

  invert(pixel: any): number {
    return this.scale.invert(pixel);
  }

  invertRange(pixels: any[]) {
    //Pixels is a non-decreasing array of pixel values
    return pixels.map((pix) => {
      return this.invert(pix);
    });
  }

  model: LinearScaleModel;
}
