"""
const _zero = /*@__PURE__*/ new Vector3( 0, 0, 0 );
const _one = /*@__PURE__*/ new Vector3( 1, 1, 1 );


setFromQuaternion( q, order, update ) {

    _matrix.makeRotationFromQuaternion( q );

    return this.setFromRotationMatrix( _matrix, order, update );

}


makeRotationFromQuaternion( q ) {

    return this.compose( _zero, q, _one );

}

compose( position, quaternion, scale ) {

		const te = this.elements;

		const x = quaternion._x, y = quaternion._y, z = quaternion._z, w = quaternion._w;
		const x2 = x + x,	y2 = y + y, z2 = z + z;
		const xx = x * x2, xy = x * y2, xz = x * z2;
		const yy = y * y2, yz = y * z2, zz = z * z2;
		const wx = w * x2, wy = w * y2, wz = w * z2;

		const sx = scale.x, sy = scale.y, sz = scale.z;

		te[ 0 ] = ( 1 - ( yy + zz ) ) * sx;
		te[ 1 ] = ( xy + wz ) * sx;
		te[ 2 ] = ( xz - wy ) * sx;
		te[ 3 ] = 0;

		te[ 4 ] = ( xy - wz ) * sy;
		te[ 5 ] = ( 1 - ( xx + zz ) ) * sy;
		te[ 6 ] = ( yz + wx ) * sy;
		te[ 7 ] = 0;

		te[ 8 ] = ( xz + wy ) * sz;
		te[ 9 ] = ( yz - wx ) * sz;
		te[ 10 ] = ( 1 - ( xx + yy ) ) * sz;
		te[ 11 ] = 0;

		te[ 12 ] = position.x;
		te[ 13 ] = position.y;
		te[ 14 ] = position.z;
		te[ 15 ] = 1;

		return this;

	}


setFromRotationMatrix( m, order = this._order, update = true ) {

    // assumes the upper 3x3 of m is a pure rotation matrix (i.e, unscaled)

    const te = m.elements;
    const m11 = te[ 0 ], m12 = te[ 4 ], m13 = te[ 8 ];
    const m21 = te[ 1 ], m22 = te[ 5 ], m23 = te[ 9 ];
    const m31 = te[ 2 ], m32 = te[ 6 ], m33 = te[ 10 ];

    switch ( order ) {

        case 'XYZ':

            this._y = Math.asin( clamp( m13, - 1, 1 ) );

            if ( Math.abs( m13 ) < 0.9999999 ) {

                this._x = Math.atan2( - m23, m33 );
                this._z = Math.atan2( - m12, m11 );

            } else {

                this._x = Math.atan2( m32, m22 );
                this._z = 0;

            }

            break;

        case 'YXZ':

            this._x = Math.asin( - clamp( m23, - 1, 1 ) );

            if ( Math.abs( m23 ) < 0.9999999 ) {

                this._y = Math.atan2( m13, m33 );
                this._z = Math.atan2( m21, m22 );

            } else {

                this._y = Math.atan2( - m31, m11 );
                this._z = 0;

            }

            break;

        case 'ZXY':

            this._x = Math.asin( clamp( m32, - 1, 1 ) );

            if ( Math.abs( m32 ) < 0.9999999 ) {

                this._y = Math.atan2( - m31, m33 );
                this._z = Math.atan2( - m12, m22 );

            } else {

                this._y = 0;
                this._z = Math.atan2( m21, m11 );

            }

            break;

        case 'ZYX':

            this._y = Math.asin( - clamp( m31, - 1, 1 ) );

            if ( Math.abs( m31 ) < 0.9999999 ) {

                this._x = Math.atan2( m32, m33 );
                this._z = Math.atan2( m21, m11 );

            } else {

                this._x = 0;
                this._z = Math.atan2( - m12, m22 );

            }

            break;

        case 'YZX':

            this._z = Math.asin( clamp( m21, - 1, 1 ) );

            if ( Math.abs( m21 ) < 0.9999999 ) {

                this._x = Math.atan2( - m23, m22 );
                this._y = Math.atan2( - m31, m11 );

            } else {

                this._x = 0;
                this._y = Math.atan2( m13, m33 );

            }

            break;

        case 'XZY':

            this._z = Math.asin( - clamp( m12, - 1, 1 ) );

            if ( Math.abs( m12 ) < 0.9999999 ) {

                this._x = Math.atan2( m32, m22 );
                this._y = Math.atan2( m13, m11 );

            } else {

                this._x = Math.atan2( - m23, m33 );
                this._y = 0;

            }

            break;

        default:

            console.warn( 'THREE.Euler: .setFromRotationMatrix() encountered an unknown order: ' + order );

    }

    this._order = order;

    if ( update === true ) this._onChangeCallback();

    return this;

}
"""
