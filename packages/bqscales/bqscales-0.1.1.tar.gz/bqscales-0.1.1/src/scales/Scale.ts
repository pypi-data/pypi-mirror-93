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

import {
  WidgetView
} from '@jupyter-widgets/base';

import {
  ScaleModel
} from './ScaleModel';


export
abstract class Scale extends WidgetView {
  render() {
    this.offset = 0;
    this.createD3Scale();
    this.createEventListeners();
  }

  protected createEventListeners() {
    this.listenTo(this.model, 'domain_changed', this.modelDomainChanged);
    this.listenTo(this.model, 'highlight_axis', this.highlightAxis);
    this.listenTo(this.model, 'unhighlight_axis', this.unhighlightAxis);
  }

  setRange(range: any[], padding=undefined) {
    this.scale.range(range);
  }

  computeAndSetDomain(array: any[], id: string) {
    this.model.computeAndSetDomain(array, id);
  }

  setDomain(array: any[], id: string) {
    this.model.setDomain(array, id);
  }

  expandDomain(oldRange: any[], newRange: any[]) {
    // Base class function. No implementation.
    // Implementation is particular to the child class
    // if you have a current range and then a new range and want to
    // expand the domain to expand to the new range but keep it
    // consistent with the previous one, this is the function you use.
  }

  protected modelDomainChanged() {
    this.scale.domain(this.model.domain);
    this.trigger('domain_changed');
  }

  protected highlightAxis() {
    this.trigger('highlight_axis');
  }

  protected unhighlightAxis() {
    this.trigger('unhighlight_axis');
  }

  protected abstract createD3Scale(): any;

  offset: number;
  scale: any;

  // Overriding super class
  model: ScaleModel;
}
